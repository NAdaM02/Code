using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerController : MonoBehaviour
{
    public float shootTime = 0.3f;
    private float lastShootTime = 0;
    private GvrReticlePointer aimCross;
    private static float healthPoint = 100f;
    public static float Health{get{return healthPoint;} set{healthPoint = value;}}
    public static int Score = 0;
    public Text scoreText;
    public Transform firepoint;

    private void Awake()
    {
        Score = 0;
        Health = 100;
    }
    // Start is called before the first frame update
    void Start()
    {
        aimCross = GetComponentInChildren<GvrReticlePointer>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        if (lastShootTime >Time.time - shootTime)
        {
            return;
        }
        var target = aimCross.CurrentRaycastResult;
        if (target.gameObject)
        {
            if (target.gameObject.tag == "Enemy"){
                Fire();
                lastShootTime = Time.time;
            }
        }
    }

    public void Fire()
    {
        var projectile = ObjectPools.Instance.GetBullet();
        projectile.transform.position = firepoint.position;
        projectile.transform.rotation = Quaternion.Euler(90, 0, 0);
        projectile.gameObject.SetActive(true);
        projectile.GetComponent<Rigidbody>().velocity = Vector3.zero;
        projectile.GetComponent<Rigidbody>().AddForce(BulletController.bulletSpeed * firepoint.transform.forward);
    }
}
