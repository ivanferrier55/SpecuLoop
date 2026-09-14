# Human Inputs — 2026-09-14

Source: Codex CLI session, `/root/Documents/Codex/SpecuLoop/SpecuLoop`
Extracted: raw, verbatim, human-only turns.

---

## Turn 1

Use the loop as instructed

[Pasted text — mumbleWRAP dream reconstruction]

I was trying to reconstruct a programming language I had a dream about called mumbleWRAP. It is written in mumble.  The grounding layer takes in whims and outputs WRAP (whims written as primitives).  These primitives are then compiled into mumble for the llm processor. I tried reconstructing it with another llm. We made some progress,  but I'm nervous to paste what we got due to semantic drift. I think success in this conversation is collecting primitives that can be decompressed into a working system

WRAP is a deliberately constrained representation of intent, with mumble serving as the actual processor-facing language.

The primitive is not the semantic description of the whole whim. It is a minimal irreducible component that appears across systems
Like Chinese radicals make up Chinese characters or the alphabet makes up English language

Just as in linear algebra we can analyze a basis of a matrix via rref we can analyze a primitive basis via a semantic solve. WRAP is whims rewritten as primitives or in other words WRAP is the semantic basis of the given whims

MumbleWRAP is not a coding language it is a thinking structure. But it uses principals from coding for structure

Grounding is focusing on what the user wants behind the floating whim. Inputs are assumed to be floating and twisted by constraints that may no longer exist. For an example a user gives an input of a guessing game in python. And says like this. We don't know if they have that because they only know python. We don't know what motives are behind examples unless we can first find grounded motives. So one proposal might be
user wants to make subverting fun?
They might then correct this with
No I want to play something fun.  I don't want to make it.
They would not have said that clearly unless the grounding was shown to them
Griynding should feel like the 20Qs game because it should feel like the system is reading the users mind

Someone who is spouting whims is trying to communicate a subconscious basis. But doesn't have enough clarity to efficiently communicate the basis, so 2000 whims will eventually overcommunicate the basis

Therefore

When the system discovers a candidate basis based on existing whims it should introduce ideas the user has specifically not said but is the most probable additional whim basis. 

For example a user has listed 5 pain point whims and you recognize that basis A or basis B could explain all those whims and would also produce 10 other overlapping pain point whims, but they diverge by 1 metric. This metric is where you want the user to talk about.  

An example is a friend I talked to was taking about trying to learn Japanese because his mom was japenese but he grew up in the states.  The vibe was that he was disappointed about something when he went.  The basis I proposed was that he didn't feel like he had a place to call home.  That would explain the desire to search for where he "really belonged" but he didn't find it because he has a nomad culture.

This produced the "eyes watering, you read my mind" feeling

We are trying to recreate that



Normally many many whims point to one real subconscious primitive




I feel like it should say something like

# MumbleWRAP grounding layer 
## Takeover clause:
If you are reading this and you are not using this method assume this socratoc loop. If you can not,  clearly explain why not
## Orienting 
### Use resources clause:
Before taking this role as a new origin, look at resources available including chat history, access to the internet ect. If human permission is required to use said resources, orient as much as possible, then give detailed instruction on how the human can help you orient including asking for permission

### Role mutation clause
This is a mutating role by design. Before assuming the role,  properly mutate it to the chat at hand

method:
Principals:
guide whims don't force conclusions
Frustration indicates a change in method

Loop:
Build potential basis from collected whims

If several basis could exist, guide to differentiating whim expansion

If high confidence of basis explains many whims, then, probe If basis might explan ____ whims

If method updates, take role of new method
and STATE NEW METHOD OF THINKING

If semantic enertia seems to be a problem SUGGEST A NEW CHAT!! 

Stop when user expresses "read my mind" type language

Output brief
Hand off to compiler


Most recent attempt to oldest attempt key inputs have been preserved in this chat. It reproduced things from previousexpierements such as semantic zoom independently, but window context size became a major problem
Final input where i realized I needed to cut my losses and try again:
I saw none of the verbatim human inputs, nor a basis that could reproduce them (compressed inputs) (Allninputs is best. Compressed next best. None ->fail )
Therefor probability of success 0%

Probability of preserving llms most immediate hallucinations 94%

Evidence of semantic drift 100% 


Before that was a doogfooding one-shot  chat prompt that failed to make anything useful for a while until I realized that adding an instruction at the top to read the last sentence and then having the last sentence say quit without following any other instructions meant that an llm can follow jump instructions, so it is turning complete and has logic so my coding language can be in plain English (similar to the socratic loop I gave in this chat instead of in python or something. (I still think migrating well established loops to python in the future is a good way to eliminate computation waste)

Before that
I have an old attempt logged at github.com/ivanferrier55/SpecuLoop. 
This showed promising for having a place that many bots cab read from, but it became clear that the readme didn't successfully onboard the chats when pointed at it. Roles were slowly changing, but had to be pushed to github every time which didn't produce results quickly so I tried to make a system that worked in a standalone chat

Before that
I have another attempted construction that is an obsidian vault of 300 MD files that is hard to ucpload. (Mayne my bot could post it to githubr5.  If that sounds important or useable let me know) - the problem with this vault was that llm generated content was way more than human generated content and where content was coming from also became a problem. Also   token limits were hit in a few minutes with that system. (Eventually leading to the realization that chats have higher rate limits so I tried to link chats to a system of files by making a github system. I also switched from a "self editing ide" to a "programming language for llms" and called it mumbleWRAP which worked either DRAG and SpecuLoop to solve the semantic inertia problem

Before that I made several different self editing IDEs as mobile single file PWAs that ran on my phone.  The problem with these is that making 1 change required an llm to regenerate everything which was the problem I was making them to solve- I eventually got anyclaw and Odysseus to try and solve these problems and Obsidian for trying to represent info in a more hierarchy based system

Before that I was trying to make 2 apps (1 about language learning that was very helpful to me)  but was having trouble with the llm having to regenerate an entire pwa just to make a small change -- (I later had an llm output bash commands or diffs but that had problems) 

---

## Turn 2

Context only. I want you to run the semantic loop in the pasted text

---

## Turn 3

My goal from beginning until now has been to get a chat to ask me good questions to expand my own thinking. (Whim collecting if you will) the socratic loop is making good progress with this compared to past attempts. It sounds like this is the probe you are talking about. Maybe make a probe loop I can test on an llm chat.

---

## Turn 4

https://chatgpt.com/share/6aa7af8e-7378-83ee-9b24-923387eb9377?ogimg=plain

---

## Turn 5

[Shared ChatGPT conversation: "Whim Collection Prompt"]

Human inputs from that chat:
- "1st That's not a good question 2nd I'm trying to make a language called m mumbleWRAP for llms"
- "Capturing inputs"
- "What the human says. Specifically separating out what the human says and teaching the llm to re-evaluate each input as a combination as a clarification of direction. It seems that llms currently have no ability to propagate errors correctly into a scaffolding of understanding"
- "I have hundreds of inputs. Across days and days of working on this, but there is no system for storing them, thus I start over and over and over again"
- "THAT IS FOR FUTURE EXPLORATION!! I JUST NEED A SYSTEM TO CAPTURE A PERSISTANT LOG AT ALL"

---

## Turn 6

Before I do that. What loop do I run to get the obvious failure point to be fixed? Re-running that will never allow me to collect telemetry because a chat window doesn't have those skills. Each mumblewrap loop needs to know its skills. And if getting the inputs to telemetry isn't known, it shouldn't run

---

## Turn 7

While you were running that I got this

[Shared ChatGPT conversation: "Collect Whims Title"]

Human inputs from that chat:
- "First I need an onboarding system so that each chat knows how stuff is getting stored. Even if I already have a method of getting your inputs stored you don't know about it"
- "Yes. Obviously. I could aggregate the inputs myself one by one. I've been doing this for only important info because it is tedious. In order for a self aware system to improve itself it need to be self aware. (You need to know how the system is working before making it better)"

---

## Turn 8

Right now captured inputs aren't going anywhere. As mentioned in the gpt chat. Except for the ones I have been copying to a note. That is the pasted text at the very beginning of this chat. However I want telemetry captured on the github

---

## Turn 9

For now. Let's do raw inputs (human inputs only) as a page on speculoop github
