def get_texts(lang):
    if lang=="german":
        return {
        "command0": "Nehmen Sie den Wasserkocher und befüllen Sie ihn mit ungefähr 1L Wasser und stellen Sie ihn wieder ab",
        "command1": "Schalten Sie den Wasserkocher an und nehmen Sie das Kaffeebehältnis",
        "command2": "Geben Sie 6 Esslöffel Kaffee in die French Press und stellen Sie das Behältnis wieder ab",
        "command3": "Wenn das Wasser gekocht hat, nehmen Sie den Wasserkocher",
        "command4": "Gießen Sie das Wasser in die French Press und stellen Sie den Wasserkocher wieder ab",
        "command5": "Warten Sie mindestens 3 Minuten, drücken Sie die French Press anschließend nach unten",
        "command6": "Nehmen Sie die French Press in die Hand",
        "command7": "Gießen Sie den Kaffee in eine Tasse und stellen Sie die French Press zurück an ihren Platz",
        "command8": "Genießen Sie Ihren Kaffee",
        "command9": "Neustart?",
        "command10": "Etwas ist schief gelaufen, bitte neustarten",
        "command11":"Um mit der Kafffeezubereitung zu beginnen, nehmen sie den Wasserkocher",
        "button_text0": "Kaffeebehälter setzen/nehmen",
        "button_text1": "French Press setzen/nehmen",
        "button_text2": "Wasserkocher setzen/nehmen",
        "button_text3": "Gefüllten Wasserkocher setzen/nehmen",
        "button_text4": "Wasser ausleeren",
        "button_text5": "Warten überspingen",
        "wrong": "Etwas ist schiefgelaufen: ",
        "reverse0": "Bitte stellen Sie den Wasserkocher wieder ab",
        "reverse1": "Bitte nehmen Sie den Wasserkocher",
        "reverse2": "Bitte stellen Sie die French Press wieder ab",
        "reverse3": "Bitte nehmen Sie die French Press",
        "reverse4": "Bitte stellen Sie das Kaffeebehältnis wieder ab",
        "reverse5": "Bitte nehmen Sie das Kaffeebehältnis",
        "heading1": "Kaffeemodell",
        "restart_button_text": "Neustart",
        "countdown_text": "Bitte warten Sie",
        "go_on_text": "Bitte fahren Sie fort!",
        "tabs": ["Modell", "Aktionsgraph"]
        }
    elif lang=="english":
        return {
        "command0":"Fill the kettle with 1L of water and put it back",
        "command1": "Start the kettle and take the coffee container",
        "command2": "Put 6 tablespoons of coffee in the French Press and put the container back",
        "command3": "When the water is boiled, take the kettle",
        "command4": "Pour the water into the French Press and put the kettle back",
        "command5": "Wait at least 3 minutes, press the French Press down afterwards",
        "command6": "Take the French Press",
        "command7": "Pour the coffee into a cup and put the French Press back in its place",
        "command8": "Enjoy your coffee",
        "command9": "Restart?",
        "command10": "Something went wrong, please restart",
        "command11":"To start the coffee preparation,take the water kettle",
        "button_text0": "Take/put the Coffee container",
        "button_text1": "Set/take French Press",
        "button_text2": "Set/take kettle",
        "button_text3": "Set/take filled kettle",
        "button_text4": "Empty kettle",
        "button_text5": "Skip Waiting",
        "wrong": "Something went wrong: ",
        "reverse0": "Please put the kettle back",
        "reverse1": "Please take the kettle",
        "reverse2": "Please put the French Press back",
        "reverse3": "Please take the French Press",
        "reverse4": "Please put the coffee container back",
        "reverse5": "Please take the coffee container",
        "heading1": "Coffee Model",
        "restart_button_text": "Restart",
        "countdown_text": "Please wait",
        "go_on_text": "Please continue",
        "tabs": ["Model", "Action Graph"]
        }

def make_state_string(state):
    stateString = ""
    for ind_state in state:
        stateString += str(ind_state)
    return stateString

def get_id_out_of_result(result, texts):
    if "Impossible state" in result:
        return 10, texts["command10"]
    result = result.split(":")[1].split("(")[0]
    result = result[1:len(result)-2]
    id, command = translate_states(result, texts)
    return id, command

def translate_states(states, texts):
    match states:
        case "Zu Beginn, den Wasserkocher nehmen":
            return 11, texts["command11"]
        case "Wasserkocher nehmen":
            return 3, texts["command0"]
        case "Wasserkocher befüllen und wieder abstellen":
            return 0, texts["command0"]  
        case "Wasserkocher anmachen, Kaffebehälter nehmen":
            return 1, texts["command1"] 
        case "Kaffeepulver in die French Press geben und Behälter abstellen":
            return 2, texts["command2"]
        case "Nach dem Kochen des Wassers, Wasserkocher nehmen":
            return 3, texts["command3"] 
        case "Wasser in die French Press geben und Wasserkocher abstellen":
            return 4, texts["command4"]
        case "3 minuten warten, dann French Press drücken":
            return 5, texts["command5"]
        case "French Press nehmen":
            return 6, texts["command6"]
        case "Kaffee servieren und French Press abstellen":
            return 7, texts["command7"]
        case "END":
            return 8, texts["command8"]
        
def get_error_command(texts, wrong_state, right_state):
    overflow_state = []
    for i in range(0,len(wrong_state)):
        overflow_state.append(wrong_state[i]-right_state[i])
    match overflow_state:
        case [1, 0, 0, 0]:
            return texts["reverse5"]
        case [-1, 0, 0, 0]:
            return texts["reverse4"]
        case [0, 1, 0, 0]:
            return texts["reverse3"]
        case [0, -1, 0, 0]:
            return texts["reverse2"]
        case [0, 0, 1, 1]:
            return texts["reverse1"]
        case [0, 0, -1, -1]:
            return texts["reverse0"]
        case _:
            return texts["command10"]