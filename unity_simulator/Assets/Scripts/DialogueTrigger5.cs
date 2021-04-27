using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DialogueTrigger5 : MonoBehaviour
{
    // Start is called before the first frame update
    public ObjectDialogue dialogue;
    public void TriggerDialogue()
    {

        FindObjectOfType<DialogueManager>().StartDialogue(dialogue);
    }
}
