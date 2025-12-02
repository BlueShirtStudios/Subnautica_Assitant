import main_config
from ai_assitant import AI_Agent

ALT = AI_Agent(api=main_config.CONFIGS["api"],
                prompt=main_config.CONFIGS["system_prompt"], 
                chat_history_file_path="../user_data/chat_history.jsonl")

#Prepare for run
ALT.intitalize_agent()
run = True

#Run ALT
while (run):
    user_question = input("What is you question? ").strip()
    if (user_question[0] == "/"):
        ALT.assit_commands.run_command(user_question)
    
    else:
        response = ALT._handle_message(user_question)
        ALT.assit_commands.deliver_Output(response)