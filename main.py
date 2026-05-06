import strawberry
from typing import List, Optional
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import random
from db import get_connection

@strawberry.type
class Quote:
    quote_id:int
    char_name:str
    quote:str
    quote_jp:Optional[str]



def get_quote_random():
    conn=get_connection()
    try:
        
        cur=conn.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) FROM quotes")
        count = cur.fetchone()["COUNT(*)"]
        if count == 0:
            return {"message": "No quotes available"}
        rand_index=random.randint(0,count-1)
        cur.execute(""" select q.quote_id,c.char_name,q.quote,q.quote_jp
            from quotes q
            inner join characters c
                    on c.char_id= q.character_id
                    LIMIT 1 OFFSET %s""", (rand_index,))
        rows=cur.fetchone()

       
        return Quote(**rows) if rows else None
    
    finally:
        cur.close()
        conn.close()



def get_quote_by_category(category:str):
    conn=get_connection()
    try:
        cur=conn.cursor(dictionary=True)
        cur.execute('''
            select q.quote_id,c.char_name,q.quote,q.quote_jp
            from quotes q
            inner join characters c
                    on c.char_id= q.character_id
            where lower(c.char_category)=lower(%s)


                ''',(category,))
        rows=cur.fetchall()

        return [Quote(**row) for row in rows]
    finally:
        cur.close()
        conn.close()

def get_quotes_by_character(char_name: str):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("""
            SELECT q.quote_id, c.char_name, q.quote, q.quote_jp
            FROM quotes q
            JOIN characters c ON c.char_id = q.character_id
            WHERE LOWER(c.char_name) = LOWER(%s)
        """, (char_name,))

        rows = cur.fetchall()
        return [Quote(**row) for row in rows]

    finally:
        cur.close()
        conn.close()


@strawberry.type
class Query:

    random_quote: Optional[Quote] = strawberry.field(
        resolver=get_quote_random
    )

    quotes_by_category: List[Quote] = strawberry.field(
        resolver=get_quote_by_category
    )

    quotes_by_character: List[Quote] = strawberry.field(
        resolver=get_quotes_by_character
    )

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


if __name__=="main":
    import uvicorn
    uvicorn.run("main:app",reload=True)