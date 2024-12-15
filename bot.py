from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
import spacy

nlp = spacy.load("en_core_web_sm")

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()

        summary, keywords = self.process_document(text)  # Process the uploaded document text
        
        informality_status = self.check_informality(text)

        await turn_context.send_activity(MessageFactory.text(f"Summary: {summary}\nKeywords: {', '.join(keywords)}\n{informality_status}"))

    def process_document(self, text):
        doc = nlp(text)
        keywords = [chunk.text for chunk in doc.noun_chunks]
        summary = ' '.join([sent.text for sent in doc.sents][:2])  # Simple summary using first two sentences
        return summary, keywords

    def check_informality(self, text):
        informal_keywords = ["gonna", "wanna", "gotta", "kinda", "sorta", "hey", "yo", "ain't", "bail", "bite", "blow", "bump", "buzz", "chill", "cool", "cram", "dude", "ditch", "flick", "flop", "freak", "gig", "gonna", "gotcha", "hang", "hit", "jive", "kinda", "lemme", "mess", "nail", "nope", "outta", "panic", "peep", "pick" , "poke", "pop", "pull", "rip", "rock", "roll", "scoop", "snoop", "snag", "suck", "swag", "tweak", "vibe", "wacky", "whip", "wipe", "yikes", "zing", "zoom", "chillax", "booze", "bummer" ,"chump", "clue", "creep", "dork", "fuzz", "geek", "grub", "hustle", "junk", "knock", "lame", "munch", "nerd", "nutty", "punk", "quirky", "riff", "savvy", "sleek"]
        informal_flag = any(word in text.lower() for word in informal_keywords)
        return "Informal language detected." if informal_flag else "Language is formal."
