import main_config
from ai_assitant import AI_Agent

ALT = AI_Agent(api=main_config.CONFIGS["api"],
                prompt=main_config.CONFIGS["system_prompt"])

ALT.intitalize_agent()
response = ALT._handle_message("Hi")
ALT.assit_commands.deliver_Output(response)