import aiosqlite

__all__ = ("create_prefix_db",)

async def create_prefix_db():
    conn = await aiosqlite.connect("data.db")
    async with conn.cursor() as c:
        try:
            await c.execute("""CREATE TABLE prefix_data (
                guild_id integer,
                prefix string
            )""")
            print("Created prefix database as it does not exist")
        except:
            print("Prefix database already exists, aborted creation job")
    return conn