no_weather_warning_messages = [
    "You're safe for today. Hooray!",
    "Don't get too comfortable; you're just lucky.",
    "You aren't being targetted by the weather gods right now."
]

"""
Chance : Forecast has a CHANCE of occuring.
NoChance : Forecast is already in occurence.
"""
forecast_messages = {
    "sunny":[
        "Better hope the sun keeps up.",
        "Nice today, ain't it?",
        "It's your lucky day.. Mostly.",
        "Don't anticipate the continued sunniness.",
        "This is pretty boring. I hope the weather shakes up.",
    ],
    "clear":[
        "Very peaceful. Be grateful.",
        "Better hope blue ain't turning gray anytime.",
        "Look at you getting all the good weather.",
        "Clear as day.",
        "VERY nice today, ain't it?"
    ],
    "cloudy": [
        "Not what I expected.",
        "Place your bet on what these clouds do next.",
        "It's a gray day. But I've got color.",
        "I wonder what comes after.",
        "Opposite of clear, simple, right?",
    ],
    "light rain":{
        "Chance":[
            "An oddity.",
            "Don't you want a drizzle?",
            "Does some rain = cold?",
            "I wish it happened.",
        ],
        "NoChance":[
            "Do you feel the droplets pecking you?",
            "My favorite weather.",
            "Let the rain drop!",
            "It may get rougher. I hope it does. :)",
            "Wear a jacket. That might save you."
        ],
    },
    "rain":{
        "Chance":[
            "I don't think you'll like this one.",
            "How do you feel if I asked it to rain a bit harshly?",
            "Oh! Please let it fall!",
            "Might be a rough one. Prepare yourself!",
        ],
        "NoChance":[
            "Tip: REALLY wear a jacket.",
            "I heard acid is in the rain droplets, is that true?",
            "Weee! The grass will grow again!",
            "If you're disappointed, too bad.",
            "Tip: Stay inside. Or don't, take the advice."
        ],
    },
    "light snow":{
        "Chance":[
            "Okay, snowing.. a little too far.",
            "If you want me to stop it; how?",
            "Even though I'm delusional, I think this is a bad sign.",
        ],
        "NoChance":[
            "You won't cause a car accident, right?",
            "Don't slip. Wear boots. Simple.",
            "Probably ain't enough for a snowman, but for sure an ice angel!",
            "It hurts, a little bit.",
        ],
    },
    "snow":{
        "Chance":[
            "OKAY THIS IS SEVERE, I SHOULD HIBERNATE.",
            "Extremely cold soon.",
            "Is this Christmas at home?",
        ],
        "NoChance":[
            "[Weather APP failed to run.]",
            "AHHHHH!! IT HURTS! ITS FREEZING! I'M GETTING FROSTBITE!",
            "Be grateful it isn't a natural disaster.",
            "This, is just fine.",
        ],
    },
    "default":[
        "What am I even reading?",
        "Does not.. compute.",
        "Fake weather, don't believe it! (I'm kidding.)",
        "Special Weather perhaps.",
    ],
}