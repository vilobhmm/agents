"""File-based queue system - atomic, crash-safe, observable.

Inspired by tinyclaw's elegant file-based queues.
Key insight: File operations are atomic, providing crash recovery for free.
"""

import json
import logging
import time
from pathlib import Path
from typing import Iterator, Optional
import uuid

from agency.core.types import MessageData, QueuedMessage


logger = logging.getLogger(__name__)


class FileQueue:
    """
    File-based message queue with atomic operations.

    Queue states:
        incoming/   - New messages waiting to be processed
        processing/ - Messages currently being processed
        outgoing/   - Responses ready to send to channels

    Benefits:
        - Atomic: File rename is atomic
        - Crash-safe: Orphaned files in processing/ recovered automatically
        - Observable: ls queue/ shows current state
        - No dependencies: Just filesystem operations
    """

    def __init__(self, queue_path: Path):
        """
        Initialize file queue.

        Args:
            queue_path: Root directory for queue
        """
        self.queue_path = Path(queue_path)
        self.incoming = self.queue_path / "incoming"
        self.processing = self.queue_path / "processing"
        self.outgoing = self.queue_path / "outgoing"

        # Create directories
        self.incoming.mkdir(parents=True, exist_ok=True)
        self.processing.mkdir(parents=True, exist_ok=True)
        self.outgoing.mkdir(parents=True, exist_ok=True)

        logger.info(f"File queue initialized at {queue_path}")

    def enqueue(self, message: MessageData, queue_type: str = "incoming") -> Path:
        """
        Add a message to the queue.

        Args:
            message: Message to enqueue
            queue_type: Queue to add to (incoming/outgoing)

        Returns:
            Path to created file
        """
        # Generate unique filename
        timestamp = int(time.time() * 1000)
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.json"

        # Select queue
        if queue_type == "incoming":
            queue_dir = self.incoming
        elif queue_type == "outgoing":
            queue_dir = self.outgoing
        else:
            raise ValueError(f"Invalid queue type: {queue_type}")

        file_path = queue_dir / filename

        # Write message as JSON
        with open(file_path, 'w') as f:
            json.dump(self._serialize_message(message), f, indent=2)

        logger.debug(f"Enqueued message to {queue_type}: {filename}")
        return file_path

    def dequeue(self) -> Optional[QueuedMessage]:
        """
        Get next message from incoming queue (atomic move to processing).

        Returns:
            QueuedMessage if available, None if queue empty
        """
        # Get oldest file in incoming
        files = sorted(self.incoming.glob("*.json"))

        if not files:
            return None

        file_path = files[0]

        # Atomic move to processing
        processing_path = self.processing / file_path.name

        try:
            file_path.rename(processing_path)
        except FileNotFoundError:
            # File was taken by another process
            return None

        # Read message
        with open(processing_path, 'r') as f:
            data = json.load(f)

        message = self._deserialize_message(data)

        return QueuedMessage(
            path=processing_path,
            data=message,
            created_at=processing_path.stat().st_ctime
        )

    def complete(self, queued_message: QueuedMessage):
        """
        Mark a message as completed (delete from processing).

        Args:
            queued_message: Message to complete
        """
        try:
            queued_message.path.unlink()
            logger.debug(f"Completed message: {queued_message.path.name}")
        except FileNotFoundError:
            logger.warning(f"Message already deleted: {queued_message.path.name}")

    def recover_orphaned(self) -> int:
        """
        Recover orphaned files in processing/ (from crashes).

        Moves files back to incoming/ if they're older than 5 minutes.

        Returns:
            Number of files recovered
        """
        recovered = 0
        now = time.time()
        threshold = 5 * 60  # 5 minutes

        for file_path in self.processing.glob("*.json"):
            age = now - file_path.stat().st_ctime

            if age > threshold:
                # Move back to incoming
                incoming_path = self.incoming / file_path.name
                file_path.rename(incoming_path)
                recovered += 1
                logger.warning(f"Recovered orphaned message: {file_path.name}")

        if recovered > 0:
            logger.info(f"Recovered {recovered} orphaned messages")

        return recovered

    def iter_outgoing(self) -> Iterator[QueuedMessage]:
        """
        Iterate over outgoing messages (for channels to poll).

        Yields:
            QueuedMessage instances from outgoing queue
        """
        for file_path in sorted(self.outgoing.glob("*.json")):
            with open(file_path, 'r') as f:
                data = json.load(f)

            message = self._deserialize_message(data)

            yield QueuedMessage(
                path=file_path,
                data=message,
                created_at=file_path.stat().st_ctime
            )

    def delete_outgoing(self, path: Path):
        """
        Delete a message from outgoing queue (after channel sends it).

        Args:
            path: Path to message file
        """
        try:
            path.unlink()
            logger.debug(f"Deleted outgoing message: {path.name}")
        except FileNotFoundError:
            logger.warning(f"Outgoing message already deleted: {path.name}")

    def get_queue_size(self, queue_type: str = "incoming") -> int:
        """
        Get number of messages in a queue.

        Args:
            queue_type: Queue to check

        Returns:
            Number of messages
        """
        if queue_type == "incoming":
            return len(list(self.incoming.glob("*.json")))
        elif queue_type == "processing":
            return len(list(self.processing.glob("*.json")))
        elif queue_type == "outgoing":
            return len(list(self.outgoing.glob("*.json")))
        else:
            return 0

    def _serialize_message(self, message: MessageData) -> dict:
        """Convert MessageData to JSON-serializable dict"""
        return {
            "channel": message.channel,
            "sender": message.sender,
            "sender_id": message.sender_id,
            "message": message.message,
            "timestamp": message.timestamp,
            "message_id": message.message_id,
            "agent": message.agent,
            "team": message.team,
            "conversation_id": message.conversation_id,
            "files": [str(f) for f in message.files],
            "metadata": message.metadata,
        }

    def _deserialize_message(self, data: dict) -> MessageData:
        """Convert dict to MessageData"""
        return MessageData(
            channel=data["channel"],
            sender=data["sender"],
            sender_id=data["sender_id"],
            message=data["message"],
            timestamp=data["timestamp"],
            message_id=data["message_id"],
            agent=data.get("agent"),
            team=data.get("team"),
            conversation_id=data.get("conversation_id"),
            files=[Path(f) for f in data.get("files", [])],
            metadata=data.get("metadata", {}),
        )
