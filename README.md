
# aiogram tortoise-orm template
**This is a template for creating Telegram bots using [aiogram](https://github.com/aiogram/aiogram) and [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/). It provides a basic structure that will allow you to quickly start developing your bot.**\
*Includes Admin panel: Mailing, Bot statistics*
## Run Locally

Clone the project

```bash
  git clone https://github.com/am1rqr/aiogram-tortoise-template
```

Go to the project directory

```bash
  cd my-project
```

Install requirements

```bash
  pip install requirements.txt
```

Start the bot

```bash
  python main.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`BOT_TOKEN`
> Token from @BotFather

`DB_URL`
> `sqlite:`     
> - *sqlite:///data/db.sqlite*
>
> `postgres:`
> - `psycopg`: *psycopg://postgres:pass@db.host:5432/somedb*
> - `asyncpg`: *asyncpg://postgres:pass@db.host:5432/somedb*
> 
> `mysql:`
> - mysql://myuser:mypass@db.host:3306/somedb
> 
> `mssql:`
> - mssql://myuser:mypass@db.host:1433/somedb?driver=the odbc driver


## Config
`admins_ids` list of admins ids
> The first one from the list will be sent notifications about turning the bot on and off
> 
> *Admin panel: **/admin***

## License

[MIT](https://choosealicense.com/licenses/mit/)