#!/usr/bin/env python
import os
import sys

import pika

from chess.piece_placer import PiecePlacer
from chess_db import sa_tables
from chess_db.queries import get_task
from chess_db.main import engine, SessionLocal

sa_tables.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='piece_placer')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        task_id = int(body)
        db = SessionLocal()
        task = get_task(db, task_id)
        task.state = "processing"
        db.commit()
        task.solution = PiecePlacer(n=task.n, piece_type=task.piece).find_placements()
        task.state = "ready"
        print(task)
        db.commit()

    channel.basic_consume(queue='piece_placer', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
