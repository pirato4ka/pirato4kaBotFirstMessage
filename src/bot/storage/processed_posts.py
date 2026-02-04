from __future__ import annotations
import aiosqlite


class ProcessedPostsRepo:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    async def init(self) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_posts (
                    channel_id INTEGER NOT NULL,
                    channel_message_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (channel_id, channel_message_id)
                );
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_media_groups (
                    channel_id INTEGER NOT NULL,
                    media_group_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (channel_id, media_group_id)
                );
                """
            )
            await db.commit()

    async def is_processed(self, channel_id: int, channel_message_id: int) -> bool:
        async with aiosqlite.connect(self._db_path) as db:
            async with db.execute(
                "SELECT 1 FROM processed_posts WHERE channel_id=? AND channel_message_id=? LIMIT 1;",
                (channel_id, channel_message_id),
            ) as cur:
                return (await cur.fetchone()) is not None

    async def mark_processed(self, channel_id: int, channel_message_id: int) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO processed_posts (channel_id, channel_message_id) VALUES (?, ?);",
                (channel_id, channel_message_id),
            )
            await db.commit()

    async def is_media_group_processed(self, channel_id: int, media_group_id: str) -> bool:
        async with aiosqlite.connect(self._db_path) as db:
            async with db.execute(
                "SELECT 1 FROM processed_media_groups WHERE channel_id=? AND media_group_id=? LIMIT 1;",
                (channel_id, media_group_id),
            ) as cur:
                return (await cur.fetchone()) is not None

    async def mark_media_group_processed(self, channel_id: int, media_group_id: str) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO processed_media_groups (channel_id, media_group_id) VALUES (?, ?);",
                (channel_id, media_group_id),
            )
            await db.commit()