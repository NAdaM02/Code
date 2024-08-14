using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BulletController : MonoBehaviour
{
    public static float bulletSpeed = 1000f;
    private static int bulletDamage = 100;
    public static int Damage{get{return bulletDamage;} set{bulletDamage = value;}}
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerEnter()
    {
        ObjectPools.Instance.RetornToPool(this);
    }
}
