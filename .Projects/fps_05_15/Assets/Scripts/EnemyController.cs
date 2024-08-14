using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyController : MonoBehaviour
{
    private float hp = 50f;
    private float dp = 10f;
    private float speed = 5f;
    public float Health {get{return hp;} set{hp = value;}}
    public float Damage {get{return dp;} set{dp = value;}}
    public float Speed {get{return speed;} set{speed = value;}}
    private Animator anim;
    private PlayerController player;
    private Vector3 offset = new Vector3(0, 1.5f, -2.5f);
    private Vector3 playerPos;
    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        player = FindObjectOfType<PlayerController>();
        playerPos = player.transform.position - offset;
    }

    // Update is called once per frame
    void Update()
    {
        transform.position += transform.forward * Speed * Time.deltaTime;
        anim.SetBool("move", true);
        if (PlayerNearby(10f))
        {
            transform.position = Vector3.MoveTowards(transform.position, playerPos, Speed * Time.deltaTime);
            transform.LookAt(playerPos);
            if (PlayerNearby(5f))
            {
                StartCoroutine(AttackPlayer());
            }
        }
        if (Health <= 0)
        {
            //MonsterDied();
        }
    }

    IEnumerator AttackPlayer()
    {
        anim.SetBool("attack", true);
        yield return new WaitForSeconds(1);
        Destroy(gameObject, 1);
    }

    private bool PlayerNearby(float value)
    {
        return Vector3.Distance(transform.position, player.transform.position) <= value;
    }
}
