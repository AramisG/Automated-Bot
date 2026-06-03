# Automated Bot

A Python-based automation bot built for a locally hosted Club Penguin-style server. This project was created to experiment with WebSocket communication, event handling, message parsing, player data storage, and command-based automation.

## Overview

The bot connects to a local game server, listens for incoming game messages, and responds to certain events with automated actions. It uses encoded Socket.IO-style messages, stores player information locally, and separates networking, protocol logic, and event handling into different files.

## Features

* Connects to a local server using WebSocket communication
* Encodes and decodes message payloads with `msgpack` and `base64`
* Sends automated game actions
* Reads incoming game messages
* Stores player data in a local JSON file
* Uses a `.env` file for private login credentials
* Separates logic across multiple Python modules for cleaner organization
