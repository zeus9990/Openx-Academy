import discord
url = "https://i.postimg.cc/tJkT3LM3/P-P.jpg"
color = 0xFFFFFF
embed_list = [
    discord.Embed(
        title="📋 Chapter 1: Introduction to Architecture (Xnode & XnodeOS)",
        description=("In this chapter you will dive into the core structure of OpenxAI a decentralized, container-based framework running on the immutable and reproducible NixOS (XnodeOS).Each Xnode is designed to securely handle critical tasks such as training, inference, and data ingestion in a fully decentralized and tamper-proof environment.\n\n"
        ">>> **How to attend the test:**\n"
        "• Answer X multiple-choice questions in this chapter.\n"
        "• Each question has a strict one-minute time limit.\n"
        "• Successfully pass all questions to earn an exclusive role that unlocks the next academy level.\n"
        "• Make sure to carefully study the provided documentation by clicking the \"Read Chapter\" button below before you jump in the test.\n"
        "⚠️ If you answer incorrectly, you must wait **1 hour** before trying again."
        ),
        color=color
    ).set_footer(
        text="For any help, contact moderators or support.",
        icon_url=url
    ).set_image(
        url="https://i.postimg.cc/J4fS2F3T/Openx-Ai-Academy-LEVEL-1.png"
    ),
    discord.Embed(
        title="📋 Chapter 2: Introduction to Data Layer",
        description=(
            "In this chapter you will find out how OpenxAI creates a truly decentralized storage solution by storing datasets and models across distributed networks like Openmesh. This ensures data persistence and censorship resistance, while AI models are tokenized as NFTs (ERC-721 / ERC-6551), granting immutable ownership and transparent provenance.\n\n"
            ">>> **How to attend the test:**\n"
            "• Answer X multiple-choice questions in this chapter.\n"
            "• Each question has a strict one-minute time limit.\n"
            "• Successfully pass all questions to earn an exclusive role that unlocks the next academy level.\n"
            "• Make sure to carefully study the provided documentation by clicking the \"Read Chapter\" button below before you jump in the test.\n"
            "⚠️ If you answer incorrectly, you must wait **1 hour** before trying again."
        ),
        color=color
    ).set_footer(
        text="For any help, contact moderators or support.",
        icon_url=url
    ).set_image(
        url="https://i.postimg.cc/tCZLDb6Z/Openx-Ai-Academy-LEVEL-2.png"
    )
]