from discord.ext import commands
import asyncio
from app.utils.gpt_interaction import get_formatted_response
from discord import Embed, Colour
import random
from discord.ext import commands
from app.utils.gpt_interaction import quiz_info


LETTER_EMOJIS = ["🇦", "🇧", "🇨", "🇩"]
CORRECT_ANSWER_INDEX = 1

quiz_states = {}


def get_question_and_options(formatted_response):
    lines = formatted_response.split("\n")
    question = lines[0].replace("Question:", "").strip()
    return question, [line.split(":")[1].strip() for line in lines[1:]]


def shuffle_and_get_correct(options):
    correct_answer = options.pop(CORRECT_ANSWER_INDEX - 1)
    random.shuffle(options)
    options.insert(random.randint(0, len(options)), correct_answer)
    return list(zip(LETTER_EMOJIS, options)), options.index(correct_answer)


def end_quiz(channel_id):
    quiz_states.pop(channel_id, None)


def is_quiz_in_progress(ctx):
    return ctx.channel.id in quiz_states


def create_quiz_embed(question, shuffled_options):
    formatted_options = "\n".join(
        [f"{emoji} {option}" for emoji, option in shuffled_options]
    )

    embed = Embed(
        title="📝 Quiz Question",
        description=f"**{question}**\n\n{formatted_options}",
        color=Colour.blue(),
    )
    embed.set_footer(text="Vous avez 60 secondes pour répondre!")
    # embed.set_thumbnail(url="URL_ICONE_QUIZ")  

    return embed


def create_feedback_embed(user, is_correct, correct_answer, url):
    if is_correct:
        description = (
            f"{user.mention} Bonne réponse !\n\nLisez plus à ce sujet [ici]({url})."
        )
        color = Colour.green()
    else:
        description = f"{user.mention} Réponse incorrecte. La bonne réponse est: {correct_answer}\n\nLisez plus à ce sujet [ici]({url})."
        color = Colour.red()

    return Embed(
        title="🔍 Résultats du Quiz",
        description=description,
        color=color,
    )


async def send_loading_message(ctx):
    return await ctx.send("⏳ Chargement du quiz...")


async def send_loading_message(ctx):
    return await ctx.send("⏳ Chargement du quiz...")


async def send_quiz_message(ctx, embed):
    msg = await ctx.send(embed=embed)
    for emoji in LETTER_EMOJIS:
        await msg.add_reaction(emoji)
    return msg


@commands.command()
async def quiz(ctx, mod: str = None, theme: str = None):
    if is_quiz_in_progress(ctx):
        await ctx.send("Un quiz est déjà en cours. Veuillez attendre qu'il se termine.")
        return

    if mod not in mod:
        await ctx.send("mod non valide.")
        return

    loading_msg = await send_loading_message(ctx)

    question, options = get_question_and_options(get_formatted_response(mod, theme))
    shuffled_options, correct_index = shuffle_and_get_correct(options)

    quiz_states[ctx.channel.id] = {
        "correct_index": correct_index,
        "url": quiz_info["current_url"],
    }

    await loading_msg.delete()
    quiz_msg = await ctx.send(embed=create_quiz_embed(question, shuffled_options))

    for emoji, _ in shuffled_options:
        await quiz_msg.add_reaction(emoji)

    def check(reaction, user):
        return (
            user == ctx.author
            and reaction.message.id == quiz_msg.id
            and str(reaction.emoji) in LETTER_EMOJIS
        )

    try:
        reaction, user = await ctx.bot.wait_for(
            "reaction_add", timeout=60.0, check=check
        )

        is_correct = (
            str(reaction.emoji)
            == shuffled_options[quiz_states[ctx.channel.id]["correct_index"]][0]
        )
        feedback = create_feedback_embed(
            user,
            is_correct,
            shuffled_options[correct_index][1],
            quiz_states[ctx.channel.id]["url"],
        )

        await ctx.send(embed=feedback)

        end_quiz(ctx.channel.id)

    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention} Temps écoulé.")
        end_quiz(ctx.channel.id)
