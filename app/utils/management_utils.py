from discord.errors import Forbidden
from discord.ext import commands


@commands.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    if not amount:
        try:
            await ctx.channel.purge(limit=100)
            await ctx.send(f"100 messages ont été supprimés !", delete_after=5)
        except Forbidden:
            await ctx.send("Je n'ai pas la permission de supprimer les messages.")
    else:
        try:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"{amount} messages ont été supprimés !", delete_after=5)
        except Forbidden:
            await ctx.send("Je n'ai pas la permission de supprimer les messages.")
