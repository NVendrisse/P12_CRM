# Epic Event CRM

A brand new command line interface app for the management of Epic Event

## Installation :

After cloning this repository

Open your terminal in administrator mode and do the following steps :

**Windows user:**
```bash
cd ..\P12_CRM
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

**MacOs or Linux user:**
```bash
cd ..\P12_CRM
python -m venv env
env/bin/activate
pip install -r requirements.txt
```

## Usage

*For any command there is a help feature*

```bash
py -m crm <command_name> --help
```

**First install**



### Users related commands

>**Log in** 

*There is an auto prompt for the login so you don't need to write your login and password in the command line*

```bash
py -m crm user login
```

>**Log out**

```bash
py -m crm user logout
```

> **Create**

Will prompt to you any needed field
```bash
py -m crm user create
```
> **Search**
```bash
py -m crm user search <filter> <search string>
```
> **Change password**
```bash
py -m crm user changepsw <login>
```
> **Rename**
```bash
py -m crm user rename <login> <options>
```
> **Delete**
```bash
py -m crm user delete <login>
```
### Client related commands

> **Create**

```bash
py -m crm client create
```

> **Search**

```bash
py -m crm client search <filter> <search string>
```

> **Update**

```bash
py -m crm client update <name> <surname> <section to update> <new value>
```

> **Get all client**

```bash
py -m crm client all
```

### Contract related commands

> **Create**

```bash
py -m crm contract create
```

> **Delete**

```bash
py -m crm contract delete <contract id>
```

> **Set the contract as payed**

```bash
py -m crm contract payment <condratc id> <optional new value : default = 0>
```

> **Search for one or more contract**

```bash
py -m crm contract search <search option> <search value>
```

> **Set a contract as signed**

```bash
py -m crm contract sign <condratc id>
```

### Event related commands

## Technology involved

ORM : Peewee  
DataBase : Sqlite3  
CLI : Typer  
Cryptography : argon2  
Authentification : JWT


## Credits
**Author :** Vendrisse Nicolas 