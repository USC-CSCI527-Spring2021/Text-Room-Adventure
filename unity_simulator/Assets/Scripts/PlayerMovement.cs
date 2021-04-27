using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    private float movementSpeed = 3f;
    private Vector2 movement;
    private Rigidbody2D rigidbody;

    private Animator anim;
    private float horizontal = 0.0f;
    private float speed = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        rigidbody = GetComponent<Rigidbody2D>();
    }

    private void Update()
    {
        movement.x = Input.GetAxisRaw("Horizontal");
        movement.y = Input.GetAxisRaw("Vertical");   

        // Debug.Log("movement.X = " + movement.x);
        // Debug.Log("movement.Y = " + movement.y);

        horizontal = movement.x > 0.01f ? movement.x : movement.x < -0.01f ? 1 : 0; // why use 1 here to make sure x be 0 or 1?
        speed = movement.y > 0.01f ? movement.y : movement.y < -0.01f ? 1 : 0;

        if(movement.x < -0.01f)
        {
            gameObject.transform.localScale = new Vector3(-1, 1, 1);
        } else 
        {
            gameObject.transform.localScale = new Vector3(1, 1, 1);
        }

        anim.SetFloat("Horizontal", horizontal);
        anim.SetFloat("Vertical", movement.y);
        anim.SetFloat("Speed", speed);
    }

    void FixedUpdate()
    {
        rigidbody.MovePosition(rigidbody.position + movement * movementSpeed * Time.fixedDeltaTime);
    }
}
