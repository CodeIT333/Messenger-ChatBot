Messenger Chat Bot

----
csomagold program telepítése:
pip install /path/to/your/package/dist/chatbot-0.1.tar.gz

----
A program elérési weboldala:
heroku url: https://immense-sea-95093-a6e0a2ea4595.herokuapp.com/

----
pylint kódelemzése:

pylint app.py
************* Module app
app.py:74:0: C0301: Line too long (108/100) (line-too-long)
app.py:93:0: C0301: Line too long (111/100) (line-too-long)
app.py:118:0: C0301: Line too long (113/100) (line-too-long)
app.py:133:0: C0301: Line too long (112/100) (line-too-long)
app.py:143:0: C0301: Line too long (107/100) (line-too-long)
app.py:238:0: C0301: Line too long (114/100) (line-too-long)
app.py:246:0: C0301: Line too long (103/100) (line-too-long)
app.py:276:0: C0301: Line too long (105/100) (line-too-long)
app.py:315:0: C0304: Final newline missing (missing-final-newline)
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:73:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:74:13: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
app.py:80:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:81:13: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
app.py:102:16: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
app.py:106:0: R0914: Too many local variables (25/15) (too-many-locals)
app.py:111:4: W0105: String statement has no effect (pointless-string-statement)
app.py:169:11: W0718: Catching too general exception Exception (broad-exception-caught)
app.py:190:17: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
app.py:195:0: R0914: Too many local variables (20/15) (too-many-locals)
app.py:209:8: C0103: Variable name "temperaureNum" doesn't conform to snake_case naming style (invalid-name)
app.py:232:0: R0914: Too many local variables (32/15) (too-many-locals)
app.py:309:4: C0103: Variable name "ENDPOINT" doesn't conform to snake_case naming style (invalid-name)
app.py:310:15: W3101: Missing timeout argument for method 'requests.post' can cause your program to hang indefinitely (missing-timeout)
app.py:11:0: C0411: standard import "os" should be placed before third party imports "selenium.webdriver", "selenium.webdriver.common.by.By", "selenium.webdriver.support.ui.WebDriverWait" (...) "flask.Flask", "pymessenger.Bot", "bs4" (wrong-import-order)
app.py:11:0: W0611: Unused import os (unused-import)

-----------------------------------
Your code has been rated at 8.35/10


----
flake8 kódelemzése:
flake8 app.py
app.py:20:1: E302 expected 2 blank lines, found 1
app.py:23:80: E501 line too long (89 > 79 characters)
app.py:74:14: F541 f-string is missing placeholders
app.py:74:80: E501 line too long (108 > 79 characters)
app.py:75:80: E501 line too long (95 > 79 characters)
app.py:81:14: F541 f-string is missing placeholders
app.py:81:80: E501 line too long (88 > 79 characters)
app.py:82:80: E501 line too long (89 > 79 characters)
app.py:93:80: E501 line too long (111 > 79 characters)
app.py:102:17: F541 f-string is missing placeholders
app.py:118:80: E501 line too long (113 > 79 characters)
app.py:133:80: E501 line too long (112 > 79 characters)
app.py:134:80: E501 line too long (98 > 79 characters)
app.py:135:80: E501 line too long (93 > 79 characters)
app.py:141:80: E501 line too long (85 > 79 characters)
app.py:143:80: E501 line too long (107 > 79 characters)
app.py:161:80: E501 line too long (83 > 79 characters)
app.py:166:80: E501 line too long (98 > 79 characters)
app.py:190:18: F541 f-string is missing placeholders
app.py:190:80: E501 line too long (87 > 79 characters)
app.py:191:80: E501 line too long (85 > 79 characters)
app.py:204:80: E501 line too long (87 > 79 characters)
app.py:214:80: E501 line too long (80 > 79 characters)
app.py:222:80: E501 line too long (82 > 79 characters)
app.py:225:80: E501 line too long (84 > 79 characters)
app.py:228:80: E501 line too long (90 > 79 characters)
app.py:238:80: E501 line too long (114 > 79 characters)
app.py:245:80: E501 line too long (87 > 79 characters)
app.py:246:80: E501 line too long (103 > 79 characters)
app.py:249:80: E501 line too long (80 > 79 characters)
app.py:253:80: E501 line too long (90 > 79 characters)
app.py:264:80: E501 line too long (86 > 79 characters)
app.py:270:80: E501 line too long (85 > 79 characters)
app.py:276:80: E501 line too long (105 > 79 characters)
app.py:285:80: E501 line too long (83 > 79 characters)
app.py:290:80: E501 line too long (98 > 79 characters)
app.py:294:80: E501 line too long (90 > 79 characters)
app.py:309:80: E501 line too long (95 > 79 characters)
app.py:315:33: W292 no newline at end of file
