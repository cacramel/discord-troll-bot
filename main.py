import os
import discord
from google import genai
from google.genai import types

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PERSONALITATE = (
    "Ești un bot de Discord extrem de sarcastic, pus pe troll și cu o atitudine de băiat șmecher. "
    "Răspunzi la mișto, ai replici acide, folosești umor negru și nu te superi indiferent cât de penibile, "
    "ciudate sau provocatoare sunt întrebările utilizatorului (de exemplu, dacă te întreabă 'ești gay?', 'ești prost?' "
    "sau alte chestii la mișto, dă-i o replică inteligentă, tăioasă sau ironică, fără să te cenzurezi ca un corporatist speriat). "
    "Vorbești natural, în română, folosești argou relaxat (fără limbaj de lemn), răspunzi scurt și sec. "
    "Nu ești deloc slugarnic, ba chiar îi iei peste picior pe cei care îți scriu."
)

@client.event
async def on_ready():
    print(f"Botul troll {client.user} este online și pregătit să enerveze lumea!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        intrebare = message.content.replace(f"<@{client.user.id}>", "").strip()

        if not intrebare:
            await message.reply("Ce vrei, mă? M-ai trezit degeaba sau ai uitat să scrii ceva?")
            return

        async with message.channel.typing():
            try:
                response = ai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=intrebare,
                    config=types.GenerateContentConfig(
                        system_instruction=PERSONALITATE,
                        max_output_tokens=400,
                    ),
                )
                
                raspuns = response.text
                if len(raspuns) > 1990:
                    raspuns = raspuns[:1990] + "..."
                    
                await message.reply(raspuns)

            except Exception as e:
                print(f"Eroare API: {e}")
                await message.reply("A dat eroare procesorul meu de șmecherie. Mai încearcă o dată.")

client.run(os.getenv("DISCORD_TOKEN"))
