import main_config
from ai_assitant import AI_Assitant

ALT = AI_Assitant(api=main_config.CONFIGS["api"],
                  prompt=main_config.CONFIGS["template_prompt"])
ALT.start_conversation()