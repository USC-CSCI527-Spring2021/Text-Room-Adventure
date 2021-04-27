using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DialogueManager : MonoBehaviour
{
    private Queue<string> sentences;
    public Text titleText;
    public Text dialogueText;
    public Animator animator;
    // Start is called before the first frame update
    void Start()
    {
        sentences = new Queue<string>();
    }
    public void StartDialogue(ObjectDialogue dialogue)
    {
        animator.SetBool("IsOpen", true);
        //Debug.Log("aaaa" + dialogue.name);
        titleText.text = dialogue.name;
        sentences.Clear();
        foreach (string sentence in dialogue.sentences)
        {
            sentences.Enqueue(sentence);
        }
        DisplayNext();
    }
    public void DisplayNext()
    {
        if (sentences.Count == 0)
        {
            EndDialogue();
            return;
        }
        string sentence = sentences.Dequeue();
        //Debug.Log(sentence);
        dialogueText.text = sentence;
    }
    void EndDialogue()
    {
        animator.SetBool("IsOpen", false);
    }
    // Update is called once per frame
}
