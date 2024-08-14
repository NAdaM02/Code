using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerTwoController : MonoBehaviour
{
    private Animator anim;
    private float rotationSpeed = 30;
    private Vector3 inputVec;
    private Vector3 targetDirection;

    private float health = 500f;
    private static float damageDealt = 25;
    public float PlayerTwoHealth{ get { return health; } set { health=value; } }
    public static float PlayerTwoDamage{ get { return damageDealt; } set { damageDealt=value; } }
    public Slider slider;
    // Start is called before the first frame update
    void Start()
    {
        health = 500;
        damageDealt = 25f;
        anim = GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        float horizontal = Input.GetAxisRaw("PlayerTwoHorizontal");
        float vertical = Input.GetAxisRaw("PlayerTwoVertical");
        inputVec = new Vector3(horizontal, 0, vertical);
        anim.SetFloat("Input X", horizontal);
        anim.SetFloat("Input Z", vertical);
        if(vertical != 0 || horizontal != 0){
            anim.SetBool("Moving",true);
        }
        else{
            anim.SetBool("Moving",false);
        }
        if(Input.GetButtonDown("PlayerTwoAttack")){
            anim.SetTrigger("Attack1Trigger");
            StartCoroutine(AnimPause(1.2f));
        }
        UpdateMovement();
    }

    IEnumerator AnimPause(float pauseTime){
        yield return new WaitForSeconds(pauseTime);
    }

    private void UpdateMovement(){
        RotateTowardMovementDirection();
        GetCameraRelativeMovement();
    }

    private void RotateTowardMovementDirection(){
        if(inputVec != Vector3.zero){
            transform.rotation = Quaternion.Slerp(
                transform.rotation,
                Quaternion.LookRotation(targetDirection),
                Time.deltaTime * rotationSpeed
            );
        }
    }

    private void GetCameraRelativeMovement(){
        Transform cameraTransform = Camera.main.transform;

        Vector3 forward = cameraTransform.TransformDirection(Vector3.forward);
        forward.y = 0;
        forward = forward.normalized;

        Vector3 right = new Vector3(forward.z, 0 , -forward.x);

        float horizontal = Input.GetAxisRaw("PlayerTwoHorizontal");
        float vertical = Input.GetAxisRaw("PlayerTwoVertical");

        targetDirection = horizontal * right + vertical * forward;
    }

    private void OnCollisionEnter(Collision collision){
        if(collision.gameObject.tag == "Player1Weapon"){
            PlayerTwoHealth -= PlayerController.PlayerDamage;
            slider.value = PlayerTwoHealth;
        }
        if(PlayerTwoHealth <= 0){
            gameObject.SetActive(false);
        }
    }

    void FootR(){}
    void FootL(){}
    void Hit(){}
}
