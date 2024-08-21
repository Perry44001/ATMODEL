#!/usr/bin/env python
# encoding: utf-8
import gradio as gr
from PIL import Image
import traceback
import re
import torch
import argparse
from transformers import AutoModel, AutoTokenizer

# README, How to run demo on different devices

# For Nvidia GPUs.
# python web_demo_2.5.py --device cuda

# For Mac with MPS (Apple silicon or AMD GPUs).
# PYTORCH_ENABLE_MPS_FALLBACK=1 python web_demo_2.5.py --device mps

# Argparser
parser = argparse.ArgumentParser(description='demo')
# parser.add_argument('--device', type=str, default='cuda', help='cuda or cpu')
parser.add_argument('--device', type=str, default='cpu', help='cuda or cpu')
args = parser.parse_args()
device = args.device
assert device in ['cuda', 'cpu']

# Load model
# if 'int4' in model_path:
#     if device == 'mps':
#         print('Error: running int4 model with bitsandbytes on Mac is not supported right now.')
#         exit()
#     model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
# else:
#     model = AutoModel.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.float16, device_map=device)
# tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
# model.eval()

# model_path = '/Volumes/ST4000NM_1/projects/parttime_job_disk/qa_ui/trained_model/bert_model'
# model = AutoModel.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.float16, device_map=device)
# tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
# tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese', trust_remote_code=True)
# model.eval()


MODEL_LIST = [
    {'name': 'Model1', 'path': '/Volumes/ST4000NM_1/projects/parttime_job_disk/qa_ui/trained_model/bert_model'}, 
    {'name': 'Model2', 'path': 'path_to_model2'}
]

ERROR_MSG = "请输入"

# Beam Form
num_beams_slider = {
    'minimum': 0,
    'maximum': 5,
    'value': 3,
    'step': 1,
    'interactive': True,
    'label': 'Num Beams'
}
repetition_penalty_slider = {
    'minimum': 0,
    'maximum': 3,
    'value': 1.2,
    'step': 0.01,
    'interactive': True,
    'label': 'Repetition Penalty'
}
repetition_penalty_slider2 = {
    'minimum': 0,
    'maximum': 3,
    'value': 1.05,
    'step': 0.01,
    'interactive': True,
    'label': 'Repetition Penalty'
}
max_new_tokens_slider = {
    'minimum': 1,
    'maximum': 4096,
    'value': 1024,
    'step': 1,
    'interactive': True,
    'label': 'Max New Tokens'    
}

top_p_slider = {
    'minimum': 0,
    'maximum': 1,
    'value': 0.8,
    'step': 0.05,
    'interactive': True,
    'label': 'Top P'    
}
top_k_slider = {
    'minimum': 0,
    'maximum': 200,
    'value': 100,
    'step': 1,
    'interactive': True,
    'label': 'Top K'    
}
temperature_slider = {
    'minimum': 0,
    'maximum': 2,
    'value': 0.7,
    'step': 0.05,
    'interactive': True,
    'label': 'Temperature'    
}

def chat(model, tokenizer, msgs, ctx, params=None, vision_hidden_states=None):
    default_params = {"num_beams":3, "repetition_penalty": 1.2, "max_new_tokens": 1024}
    if params is None:
        params = default_params
    try:
        # model, tokenizer = app_session.get('model')
        # image = img.convert('RGB')
        answer = model.chat(
            # image=image,
            msgs=msgs,
            tokenizer=tokenizer,
            **params
        )
        res = re.sub(r'(<box>.*</box>)', '', answer)
        res = res.replace('<ref>', '')
        res = res.replace('</ref>', '')
        res = res.replace('<box>', '')
        answer = res.replace('</box>', '')
        return 0, answer, None, None
    except Exception as err:
        print(err)
        traceback.print_exc()
        return -1, ERROR_MSG, None, None


def upload_img(image, _chatbot, _app_session):
    image = Image.fromarray(image)

    _app_session['sts']=None
    _app_session['ctx']=[]
    _app_session['img']=image 
    _chatbot.append(('', 'Image uploaded successfully, you can talk to me now'))
    return _chatbot, _app_session


def respond(app_session, _question, _chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature):
    _context = [{"role": "user", "content": _question}] 
    print('<User>:', _question)

    model = app_session['model']
    tokenizer = app_session['tokenizer']
    code, _answer, _, sts = chat(model, tokenizer, _context, None)
    print('<Assistant>:', _answer)

    _context.append({"role": "assistant", "content": _answer}) 
    _chat_bot.append((_question, _answer))
    if code == 0:
        _app_cfg['ctx']=_context
        _app_cfg['sts']=sts
    return '', _chat_bot, _app_cfg


def regenerate_button_clicked(_question, _chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature):
    if len(_chat_bot) <= 1:
        _chat_bot.append(('Regenerate', 'No question for regeneration.'))
        return '', _chat_bot, _app_cfg
    elif _chat_bot[-1][0] == 'Regenerate':
        return '', _chat_bot, _app_cfg
    else:
        _question = _chat_bot[-1][0]
        _chat_bot = _chat_bot[:-1]
        _app_cfg['ctx'] = _app_cfg['ctx'][:-2]
    return respond(_question, _chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature)


def load_model(name):
    for model in MODEL_LIST:
        if model['name'] == name:
            model = AutoModel.from_pretrained(model['path'], trust_remote_code=True, torch_dtype=torch.float16, device_map=device)
            # tokenizer = AutoTokenizer.from_pretrained(model['path'], trust_remote_code=True)
            tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese', trust_remote_code=True)
            model.eval()
            return model, tokenizer
    return None

def model_selected(name, model_info_box, app_session):
    model, tokenizer = load_model(name)
    if model:
        app_session['model'] = model
        app_session['tokenizer'] = tokenizer
        # return f'Model {name} loaded successfully', app_session
        return f'模型 {name} 加载成功', app_session
    else:
        # return 'Failed to load the model', app_session
        return '模型加载失败', app_session


with gr.Blocks() as demo:
    with gr.Row():

        app_session = gr.State({'sts':None,'ctx':None,'img':None})

        with gr.Column(scale=1, min_width=300):
            # model_selector = gr.Dropdown(label="Select Model", choices=[model['name'] for model in MODEL_LIST])
            model_selector = gr.Dropdown(label="选择模型", choices=[model['name'] for model in MODEL_LIST])
            # model_info_box = gr.Textbox(label="Model Info", placeholder="No model loaded", interactive=False)
            model_info_box = gr.Textbox(label="模型信息", placeholder="", interactive=False)

            model_selector.change(
                model_selected, 
                [model_selector, model_info_box, app_session], 
                [model_info_box, app_session]
            )
        with gr.Column(scale=3, min_width=500):
            # bt_pic = gr.Image(label="Upload an image to start")
            # chat_bot = gr.Chatbot(label=f"Chat with {model_name}")
            chat_bot = gr.Chatbot(label=f"对话")
            # txt_message = gr.Textbox(label="Input text")
            txt_message = gr.Textbox(label="输入问题")
            
            txt_message.submit(
                respond, 
                [app_session, txt_message, chat_bot, app_session], 
                [app_session, txt_message, chat_bot, app_session]
            )
            # bt_pic.upload(lambda: None, None, chat_bot, queue=False).then(upload_img, inputs=[bt_pic,chat_bot,app_session], outputs=[chat_bot,app_session])


# launch
# demo.launch(share=False, debug=True, show_api=False, server_port=8080, server_name="0.0.0.0")
demo.launch(share=False, debug=True, show_api=False, server_port=9956, server_name="0.0.0.0")

