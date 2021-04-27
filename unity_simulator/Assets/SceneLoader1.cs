using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneLoader1 : MonoBehaviour
{
    public Animator transition;
    public Transform target;
    public float transitionTime = 1f;
    public int PrevScene;
    public bool triggertag1;
    public bool triggertag2;
    public bool triggertag3;
    public bool triggertag4;
    public bool triggertag5;
    public bool triggertag6;
    void Start()
    {
        triggertag1 = true;
        triggertag2 = true;
        triggertag3 = true;
        triggertag4 = true;
        triggertag5 = true;
        triggertag6 = true;

    }
    // Update is called once per frame
    void Update()
    {
        PrevScene = SceneManager.GetActiveScene().buildIndex;
            if (target.position.x > 13 && target.position.y > -8 && target.position.x < 16 && target.position.y < -6 && triggertag1 == true)
            {
                Debug.Log("trigger1");
                FindObjectOfType<DialogueTrigger>().TriggerDialogue();
                triggertag1 = false;
            }
            if (target.position.x > 13 && target.position.y > -35 && target.position.x < 16 && target.position.y < -32 && triggertag2 == true)
            {
                Debug.Log("trigger2");
                FindObjectOfType<DialogueTrigger2>().TriggerDialogue();
                triggertag2 = false;
            }
            if (target.position.x > 13 && target.position.y > -57 && target.position.x < 16 && target.position.y < -55 && triggertag3 == true)
            {
                Debug.Log("trigger3");
                FindObjectOfType<DialogueTrigger3>().TriggerDialogue();
                triggertag3 = false;
            }
            if (target.position.x > 13 && target.position.y > -71 && target.position.x < 16 && target.position.y < -69 && triggertag4 == true)
            {
                Debug.Log("trigger4");
                FindObjectOfType<DialogueTrigger4>().TriggerDialogue();
                triggertag4 = false;
            }
            if (target.position.x > 18 && target.position.y > -67 && target.position.x < 20 && target.position.y < -65 && triggertag5 == true)
            {
                Debug.Log("trigger5");
                FindObjectOfType<DialogueTrigger5>().TriggerDialogue();
                triggertag5 = false;
            }
            if (target.position.x > 22 && target.position.y > -55 && target.position.x < 24 && target.position.y < -53 && triggertag6 == true)
            {
                Debug.Log("trigger6");
                FindObjectOfType<DialogueTrigger6>().TriggerDialogue();
                triggertag6 = false;
            }
    }

    public void LoadNextScene(int levelIndex)
    {
        StartCoroutine(LoadLevel(levelIndex));
    }

    IEnumerator LoadLevel(int levelIndex)
    {
        transition.SetTrigger("Start");
        yield return new WaitForSeconds(transitionTime);
        SceneManager.LoadScene(levelIndex);
    }
}
