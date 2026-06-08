import tkinter as tk
from tkinter import ttk, scrolledtext
from chatbot import TwinCitiesChatbot

class RideFareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Twin Cities Ride Fare Assistant 🚕")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f2f5")
        
        self.chatbot = TwinCitiesChatbot()
        
        # Colors
        self.bg_color = "#f0f2f5"
        self.sidebar_color = "#ffffff"
        self.accent_color = "#0078d4"
        self.user_bubble = "#dcf8c6"
        self.bot_bubble = "#ffffff"
        
        self._setup_ui()
        self._add_welcome_message()

    def _setup_ui(self):
        # Main Container
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(self.main_container, width=250, bg=self.sidebar_color, padx=20, pady=20)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="Twin Cities Guide", font=("Segoe UI", 16, "bold"), 
                 bg=self.sidebar_color, fg=self.accent_color).pack(pady=(0, 20))
        
        categories = [
            ("🍔 Food Points", "food"),
            ("🚇 Metro Stations", "metro"),
            ("🌳 Parks & Picnic", "park"),
            ("🏙️ Pindi Areas", "pindi"),
            ("🏙️ Isloo Sectors", "islamabad")
        ]
        
        for label, cmd_arg in categories:
            btn = tk.Button(self.sidebar, text=label, font=("Segoe UI", 11), 
                            bg="#f8f9fa", fg="#333", relief=tk.FLAT, pady=10, cursor="hand2",
                            command=lambda a=cmd_arg: self._quick_action(a))
            btn.pack(fill=tk.X, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#e9ecef"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#f8f9fa"))

        # Chat Area Container
        self.chat_container = tk.Frame(self.main_container, bg=self.bg_color)
        self.chat_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat History
        self.chat_history = scrolledtext.ScrolledText(self.chat_container, wrap=tk.WORD, 
                                                    font=("Segoe UI", 12), bg=self.bg_color, 
                                                    padx=20, pady=20, borderwidth=0)
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)
        
        # Input Area
        self.input_frame = tk.Frame(self.chat_container, bg="#ffffff", pady=15, padx=20)
        self.input_frame.pack(fill=tk.X)
        
        self.user_input = tk.Entry(self.input_frame, font=("Segoe UI", 12), 
                                 bg="#f0f2f5", borderwidth=0, highlightthickness=1,
                                 highlightbackground="#ced4da", highlightcolor=self.accent_color)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.user_input.bind("<Return>", lambda e: self._send_message())
        
        self.send_btn = tk.Button(self.input_frame, text="Send ➔", font=("Segoe UI", 11, "bold"),
                                bg=self.accent_color, fg="white", relief=tk.FLAT, 
                                padx=20, pady=5, cursor="hand2", command=self._send_message)
        self.send_btn.pack(side=tk.RIGHT)

    def _quick_action(self, category):
        msg = f"Show me {category}"
        self._display_message("You", msg, is_user=True)
        response = self.chatbot.process_message(msg)
        self._display_message("Bot", response)

    def _send_message(self):
        msg = self.user_input.get().strip()
        if not msg:
            return
            
        self.user_input.delete(0, tk.END)
        self._display_message("You", msg, is_user=True)
        
        # Process with chatbot
        response = self.chatbot.process_message(msg)
        self._display_message("Bot", response)

    def _display_message(self, sender, message, is_user=False):
        self.chat_history.config(state=tk.NORMAL)
        
        tag = "user" if is_user else "bot"
        prefix = "👤 You: " if is_user else "🤖 Bot: "
        
        self.chat_history.insert(tk.END, f"\n{prefix}\n", tag + "_header")
        self.chat_history.insert(tk.END, f"{message}\n", tag + "_body")
        self.chat_history.insert(tk.END, "━" * 40 + "\n", "separator")
        
        # Styling
        self.chat_history.tag_config("user_header", font=("Segoe UI", 10, "bold"), foreground="#555")
        self.chat_history.tag_config("bot_header", font=("Segoe UI", 10, "bold"), foreground=self.accent_color)
        self.chat_history.tag_config("user_body", lmargin1=20, lmargin2=20, spacing1=5, spacing3=5)
        self.chat_history.tag_config("bot_body", lmargin1=20, lmargin2=20, spacing1=5, spacing3=5)
        self.chat_history.tag_config("separator", foreground="#ced4da")
        
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def _add_welcome_message(self):
        welcome = """Salaam! 🙋‍♂️ I'm your Twin Cities Ride Fare Assistant.

I can help you find prices for Cars, AC Cars, Luxury rides, and Bikes in Islamabad and Pindi.

Try asking: 'Savour Saddar to Centaurus' or '10km bike fare'"""
        self._display_message("Bot", welcome)

if __name__ == "__main__":
    root = tk.Tk()
    app = RideFareGUI(root)
    root.mainloop()
