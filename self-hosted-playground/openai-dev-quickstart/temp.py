import datetime
from gpt_oss.tools.simple_browser import SimpleBrowserTool
from gpt_oss.tools.simple_browser.backend import ExaBackend
from openai_harmony import SystemContent, Message, Conversation, Role, load_harmony_encoding, HarmonyEncodingName

encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)

# Exa backend requires you to have set the EXA_API_KEY environment variable
backend = ExaBackend(
    source="web",
)
browser_tool = SimpleBrowserTool(backend=backend)

# create a basic system prompt
system_message_content = SystemContent.new().with_conversation_start_date(
    datetime.datetime.now().strftime("%Y-%m-%d")
)

# if you want to use the browser tool
use_browser_tool = False
if use_browser_tool:
    # enables the tool
    system_message_content = system_message_content.with_tools(browser_tool.tool_config)
    # alternatively you could use the following if your tool is not stateless
    system_message_content = system_message_content.with_browser_tool()

# construct the system message
system_message = Message.from_role_and_content(Role.SYSTEM, system_message_content)

# create the overall prompt
messages = [system_message, Message.from_role_and_content(Role.USER, "What's the weather in SF?")]
conversation = Conversation.from_messages(messages)

# convert to tokens
token_ids = encoding.render_conversation_for_completion(conversation, Role.ASSISTANT)

# perform inference
# ...

# parse the output
messages = encoding.parse_messages_from_completion_tokens(output_tokens, Role.ASSISTANT)
last_message = messages[-1]
if last_message.recipient.startswith("browser"):
  # perform browser call
  response_messages = await browser_tool.process(last_message)

  # extend the current messages and run inference again
  messages.extend(response_messages)