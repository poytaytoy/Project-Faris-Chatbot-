## Overview

The Faris project for the system containing Faris. Faris is an AI chatbot powered by ChatGPT 3.5 and Live2D Web SDK paired with the React Framework. As of now, it can talk about typical conversations and answer questions as you would expect from ChatGPT. It was largely inspired by Neuro-sama at the time, and being a programmer, I’ve also given it the ability to display code.

Preview of Website:

<div align="center">
  <h3>Preview of Website</h3>
  <a href="https://www.youtube.com/watch?v=J1HXEZb63B8">
    <img src="https://img.youtube.com/vi/J1HXEZb63B8/maxresdefault.jpg" alt="Project Faris Preview Thumbnail" width="600" />
    <br />
    <sub>(Click to view preview)</sub>
  </a>
</div>

---

## Current Status

Note as of Jan 8 2026,

It has been 3 years, and I have overhauled this project for deployment. ChatGPT 3.5 has now been updated to use Groq’s Llama 8b instant parameter model, and the Flask server has been switched to FastAPI. Much of the backend logic has been rewritten, but the React frontend remains largely unchanged. Various UI elements have been removed because they were unfinished features, and sentiment-based expressions no longer exist as the newer model does not support expressions. If you wish to check out the new changes, check out the deployment link here:

**[https://project-faris-chatbot.vercel.app/](https://project-faris-chatbot.vercel.app/)**

This project is outdated, since many new technologies have emerged in the midst of the AI boom. There are now React libraries that do the Live2D Web SDK heavy lifting for you, rather than me porting the entire Typscript SDK over and grinding Chinese forums to get it working. Furthermore, WebRTC technologies like Livekit has made component of sending a .wav file over to the frontend obsolete, as it allows for essentially real-time streaming and response from chatbots.

For these reasons, this project is considered completed in its own sense. It has became a testimony of time of a fun little project for a once huge Neuro-sama fan. Perhaps one day, I shall make a 2.0.

