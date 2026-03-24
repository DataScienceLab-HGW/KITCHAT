import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from StatePredictionModel import PredictionModel
from time import sleep
import random
import pandas as pd
import datetime as dt
import sys

# relative imports
from utils import get_texts, make_state_string, get_id_out_of_result, get_error_command
from sensor_functions import setup_serial_com, compute_data_and_state #setup_socket, compute_data_and_state
from graph_configuration import define_edges, define_nodes, define_config, green, yellow

from LLMTTS import LLMTTS

# global streamlit configs
st.set_page_config(
    page_title="Kaffeemodell",
    page_icon="☕",
    layout="wide",
)

# global variables

if sys.argv[1] == 'simulation':
    simulation = True
else:
    simulation = False

# create the LLM - TTS object
assistant = LLMTTS(
    api_key="GJksvW162RY0py9Mt3b3pzXdQbHXpiPh",
    base_url="https://apphubai.wolke.uni-greifswald.de/v1"
)


stateString = "Start"
right_way = [ "1110","1100", "1111", "0111", "1111", "1101", "1110", "1011","1011", "1111","1111"]

# persistent state for modell in streamlit
if "states" not in st.session_state:
    st.session_state.states = [[1,1,1,0]] #[[1,1,0,0]]
if "coffee_model" not in st.session_state:
    st.session_state.coffee_model = PredictionModel()
if "language" not in st.session_state:
    st.session_state.language = "english"#"german"
if not simulation and "serial_com" not in st.session_state:
    st.session_state.serial_com = setup_serial_com('/dev/ttyACM0')#change if needed
if "weights" not in st.session_state:
    st.session_state.weights = pd.DataFrame(columns=['Zeitstempel','Kaffeebehälter', 'French Press', 'Wasserkocher'])
if "nodes" not in st.session_state:
    st.session_state.nodes = []
if "edges" not in st.session_state:
    st.session_state.edges = []
if "config" not in st.session_state:
    st.session_state.config = Config(height=1000, width=2000, physics=False, hierarchical=False)
if "state_counter" not in st.session_state:
    st.session_state.state_counter = 0
if "correct" not in st.session_state:
    st.session_state.correct = False

# texts in specific language, default is german
texts = get_texts(st.session_state.language)
# initial graph configuration
st.session_state.edges = define_edges(st.session_state.coffee_model, texts)
st.session_state.nodes = define_nodes(st.session_state.coffee_model, texts)
width = 1800
height = 1000
st.session_state.config = define_config(width, height)

# calling sensor functions to get data
def gather_sensor_data(isInitial = False):
    if isInitial:
        return make_state_string([1,1,1,0])
    current_state, st.session_state.weights  = compute_data_and_state(st.session_state.serial_com, st.session_state.weights)
    if current_state != st.session_state.states[-1]:
        st.session_state.states.append(current_state)
        stateString = make_state_string(st.session_state.states[-1])
        return stateString
    else:
        return None

# update in simulation mode
def update_state_simulation(toggled_button):
    newState = st.session_state.states[-1].copy()
    if toggled_button == 3:
        newState[2] = 1 - newState[2]
        newState[3] = 1
    else:
        newState[toggled_button] = 1 - newState[toggled_button]
    
    print(f"Toggled btn:{toggled_button}")
    print(f"NewState: {newState} ")
    print(f"{type(newState)}")
    print(f"NewState[toggled_button]:{newState[toggled_button]}")

   
    st.session_state.states.append(newState)

    print(st.session_state.states)
    stateString = make_state_string(st.session_state.states[-1])
    return stateString

# main routine streamlit UI
def main():
    N = 1*60#3*60
    col1, col2, col3= st.columns([1, 1, 40])
    with col1:
        if st.button("🇬🇧") and st.session_state.language != "english":
            st.session_state.language = "english"
            st.session_state.coffee_model = PredictionModel()
            st.rerun()
    with col2:
        if st.button("🇩🇪") and st.session_state.language != "german":
            st.session_state.language = "german"
            st.session_state.coffee_model = PredictionModel()
            st.rerun()
    with col3:
        if st.button(texts["restart_button_text"]):
            st.session_state.coffee_model = PredictionModel()
            st.session_state.states = [[1,1,1,0]]
            st.rerun()
    st.header(texts["heading1"])
    ph = st.empty()
    placeholder = st.empty()
    ph2 = st.empty()
    if simulation:
        #print(st.session_state.states)
        stateString = make_state_string(st.session_state.states[-1])
        placeholder, divider, operators  = st.columns([5, 0.1, 1])
        with operators:
            st.write("##")
            if st.button(texts["button_text0"]) and not st.session_state.correct:
                stateString = update_state_simulation(0)
            if st.button(texts["button_text1"])  and not st.session_state.correct:
                stateString = update_state_simulation(1)
            if st.button(texts["button_text2"]) and not st.session_state.correct:  # button for put/take kettle (not filled up)
                stateString = update_state_simulation(2)
            if st.button(texts["button_text3"]) and not st.session_state.correct: #set/take filled kettel
                stateString = update_state_simulation(3)
            # if st.button(texts["button_text4"]):
            #     stateString = update_state_simulation(3)
            st.write("##")
            st.image("./images/" + stateString + ".png")
        with divider:
            st.write("##")
            st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 1000px;
                        margin: auto;
                    }
                </style>
            '''

        )
        print(st.session_state.states)
        result = st.session_state.coffee_model.make_prediction_on_observation(stateString)
        print(result)
        result_id, result_command = get_id_out_of_result(result, texts)

        print(f"ResultID: {result_id}")
        
        # error handling, frag nicht was hier passiert, wir müssen nochmal das Model überarbeiten
        print("stst: " + stateString + "; right_way: " + right_way[st.session_state.state_counter])
        if result_id == 10 and not st.session_state.correct:
            st.session_state.correct = True
            wrong_state = st.session_state.states[-1]
            if len(st.session_state.states) > 1:
                st.session_state.states = st.session_state.states[0:-1]
                error_command = get_error_command(texts, wrong_state, st.session_state.states[-1])
                result_command = texts["wrong"] + error_command
                print("reset")
                st.session_state.coffee_model = PredictionModel()
                if st.session_state.state_counter != 0:
                    for i in range(0,st.session_state.state_counter-1):
                        st.session_state.coffee_model.make_prediction_on_observation(right_way[i])
                else:
                    st.session_state.coffee_model = PredictionModel()
                    st.session_state.states = [[1,1,1,0]]
                    st.rerun()
        st.session_state.state_counter += 1


        with placeholder.container():
            modell, graphtab = st.tabs(texts["tabs"])
            with modell:
                st.write("##")
                st.markdown(""" <div>
                                    <h1 
                                        style=
                                        'text-align: center;
                                        border-style: solid;
                                        background-color: #BBB;'
                                    > 
                                        {} 
                                    </h1>
                                </div>
                            """.format(result_command), unsafe_allow_html=True)
                assistant.speak(f"Write a polite message to an elderly person which says {result_command}. Output only the message and do not include any greetings, etc. Keep it short. Context is coffee preparation.")          
            with graphtab:
                if stateString != "Start":
                    for node in st.session_state.nodes:
                        if node.id == result_id:
                            node.color = green
                        else:
                            node.color = yellow
                    st.write("#")
                    agraph(st.session_state.nodes, st.session_state.edges, st.session_state.config)#, key=str(hash))
        if result_id == 5:
            if ph2.button(texts["button_text5"]):
                st.rerun()
            for secs in range(N,0,-1):
                mm, ss = secs//60, secs%60
                ph.metric(texts["countdown_text"], f"{mm:02d}:{ss:02d}")
                sleep(1)
            ph.write("Fahren Sie fort!")
            st.rerun()
    else:
        initial_run = True
        while True:
            stateString = gather_sensor_data(isInitial = initial_run)
            if stateString == None and not initial_run:
                sleep(1)
                continue
            else:
                if initial_run:
                    initial_run = False
                    stateString = make_state_string(st.session_state.states[-1])
                result = st.session_state.coffee_model.make_prediction_on_observation(stateString)
                result_id, result_command = get_id_out_of_result(result, texts)
                with placeholder.container():
                    modell, graphtab = st.tabs(texts["tabs"])
                    with modell:
                        st.write("##")
                        st.write("##")
                        st.write("##")
                        st.write("##")
                        st.markdown(""" <div>
                                            <h1 
                                                style=
                                                'text-align: center;
                                                border-style: solid;
                                                background-color: #BBB;'
                                            > 
                                                {} 
                                            </h1>
                                        </div>
                                    """.format(result_command), unsafe_allow_html=True)
                    
                        assistant.speak(f"Write a polite message to an elderly person which says {result_command}. Output only the message and do not include any greetings, etc. Keep it short.Context is coffee preparation.")
                    
                if result_id == 5:
                    for secs in range(N,0,-1):
                        mm, ss = secs//60, secs%60
                        ph.metric(texts["countdown_text"], f"{mm:02d}:{ss:02d}")
                        sleep(1)
                        ph.write(texts["go_on_text"])
                    assistant.speak(f"COmmunicate that the waiting time is over and the french press is ready to be activated.Output only the message to the user.")
                    st.rerun()
            sleep(1)
            

if __name__ == "__main__":
    main()