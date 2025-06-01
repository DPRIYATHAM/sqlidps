# sqlidps
### SQL Injection - Detection and Prevention System

SQLIDPS is a tool designed to detect and prevent SQL injection attacks in web applications. SQL injection is a common attack vector that allows attackers to execute arbitrary SQL code on a database, potentially leading to data breaches and other security issues. This project aims to provide a robust solution for identifying and mitigating such vulnerabilities.

### Flow Chart
The data flow in SQLIDPS illustrates how user inputs are processed to detect and prevent SQL injection attacks.  
Below is a detailed visualization of the flow:

![Flowchart](https://raw.githubusercontent.com/DPRIYATHAM/sqlidps/main/flowchart.png)

> Time taken to Check/parse data for sqli => **3.5ms**

## Usage

### `SQLi.check(data)`

Checks if the provided `data` contains potential SQLi payloads. Raises `PotentialSQLiPayload` if a malicious input is detected.

* **Arguments**:

  * `data` (str | list | dict): Input to be checked.

* **Example**:

```python
from sqli_dps import SQLi

try:
    SQLi.check("SELECT * FROM users WHERE '1'='1'")
except PotentialSQLiPayload as e:
    print("Blocked:", e)
```
### `SQLi.parse(data: dict, error="potential payload") → dict`

Parses a dictionary and replaces any malicious values with a safe error string instead of raising an exception.

* **Arguments**:

  * `data` (dict): Dictionary to scan.
  * `error` (str): Replacement string for detected payloads (default: `"potential payload"`).

* **Returns**:

  * A cleaned dictionary with malicious values replaced.

* **Example**:
```python
data = {
    "username": "admin",
    "password": "' OR '1'='1"
}

cleaned = SQLi.parse(data)
print(cleaned)
# Output: {'username': 'admin', 'password': 'potential payload'}
```
## Installing 
```bash
pip install sqlidps
```

## Build from Source
```bash
cd sqlidps
pip install -r requirements.txt
flex sqlidps/lexer.l -o sqlidps/lex.yy.c
make sqlidps && make sqlidps clean
python sqlidps/train.py
pip install .
```

