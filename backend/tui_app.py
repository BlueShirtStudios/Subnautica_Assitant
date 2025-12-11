from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Input
from textual.containers import Container
from datetime import datetime

import main_config
from ai_assitant import AI_Agent

ALT = AI_Agent(api=main_config.CONFIGS["api"],
                prompt=main_config.CONFIGS["system_prompt"], 
                chat_history_file_path="../user_data/chat_history.jsonl")

ALT.intitalize_agent()

class TerminalApp(App):
    CSS_PATH = "tui_styles.css"
    
    def __init__(self):
        super().__init__()
        self.chat_history = ""
        self.log_history = "12:01 - Initializing Agent\n12:02 - System Check Complete\n..."
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        #Make main panel containing 3 separate panels
        with Container(id="app_grid"):
            
            #Left Panel - Status Bar
            with Container(id="status_panel", classes="app_panel"):
                yield Static("[b]SYSTEM STATUS[/b]", classes="heading")
                yield Static("O2 Level: 95%\nPower: Operational\nDepth: 120m", id="metrics")
                yield Static("\n[i]-- Subnautica Fictional Info --[/i]", id="fictional_info")
                
            #Middle Panel - Chat Interface
            with Container(id="chat_panel", classes="app_panel"):
                yield Static("", id="chat_display")
                with Container(id="input_area"):
                    yield Input(placeholder="How can I assist you today?", id="user_input")
                    yield Button("SEND", id="send_button", variant="primary")
                
                
            #Right Panel - Chat History
            with Container(id="history_panel", classes="app_panel"):
                yield Static("[b]Transmission Log[/b]", classes="heading")
                yield Static("12:01 - Initializing Agent\n12:02 - System Check Complete\n...", id="log_content")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "send_button":
            self.send_message()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.send_message()
    
    def send_message(self) -> None:
        #Get Input from the widgey
        input_widget = self.query_one("#user_input", Input)
        message = input_widget.value.strip()
        
        if not message:
            return
        
        #Get the chat display and log widgets
        chat_display = self.query_one("#chat_display", Static)
        log_content = self.query_one("#log_content", Static)
        
        #Add user message to chat history
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_history += f"\n[cyan]You ({timestamp}):[/cyan] {message}\n[green]Agent:[/green] Message received. Processing..."
        if message[0] == '/':
            ALT.assit_commands.run_command(message)
            
        else:
            response = ALT._handle_message(message)
            
        
            chat_display.update(self.chat_history)
        
            #Add to transmission log
            self.log_history += f"\n{timestamp} - User: {message}"
            log_content.update(self.log_history)
        
            #Clear the input field
            input_widget.value = ""
        
            #Scroll chat to bottom
            chat_display.scroll_end(animate=False)

        
        
if __name__ == "__main__":
    app = TerminalApp()
    app.run()