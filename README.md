# GPTChatBot
A personal assistant bot with a voice interface powered by OpenAI APIs.

## Dependencies
Windows:<br>
`pip3 install -r requirements.txt`<br><br>
Linux:<br>
`sudo chmod +x install.sh`<br>
`./install.sh`

## Set OpenAI API key
Create your OpenAI API key here: https://platform.openai.com/account/api-keys<br><br>
Set your OpenAI API key as a system environment variable:<br>
Windows:<br>
`set OPENAI_KEY=<YOUR KEY>`<br><br>
Linux:<br>
`export OPENAI_KEY=<YOUR KEY>`

## Run
`python3 main.py`

## Usage
After running the main program, you can activate it by saying 'Hi Jarvis'. To cancel the conversation at any time, simply say 'nothing' or 'never mind', and it will return to hibernation until the next wake-up phrase.

## Derivative Works
Feel free to submit merge requests or start discussions. The implementation is currently quite basic, and please refrain from using it for repackaged commercial purposes.
