using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectPools : MonoBehaviour
{
    public BulletController bullet_prefab;
    private Queue<BulletController> bullets = new Queue<BulletController>();
    public static ObjectPools Instance{get; set;}

    private void Awake()
    {
        Instance = this;
    }

    public BulletController GetBullet()
    {
        if (bullets.Count == 0)
        {
            BulletController projectile = Instantiate(bullet_prefab);
            projectile.gameObject.SetActive(false);
            bullets.Enqueue(projectile);
        }
        return bullets.Dequeue();
    }

    public void RetornToPool(BulletController bullet)
    {
        bullet.gameObject.SetActive(false);
        bullets.Enqueue(bullet);
    }
}
