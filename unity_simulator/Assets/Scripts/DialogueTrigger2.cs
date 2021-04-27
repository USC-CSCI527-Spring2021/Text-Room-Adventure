using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DialogueTrigger2 : MonoBehaviour
{
    public ObjectDialogue dialogue;
    public void TriggerDialogue()
    {

        FindObjectOfType<DialogueManager>().StartDialogue(dialogue);
    }
}
