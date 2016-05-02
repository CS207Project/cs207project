#!/usr/bin/env python3
""" This is a utility file that starts a web server with some default settings.
It is meant to be an example of how to start our system and also servers as a way for us to test
our code.

IF YOU EDIT THIS FILE TESTS MIGHT BREAK. IT IS MEANT AS A DEMO ONLY.

"""
from webserver import WebServer

def main():
    ws = WebServer()
    ws.run()

if __name__=='__main__':
    main()
