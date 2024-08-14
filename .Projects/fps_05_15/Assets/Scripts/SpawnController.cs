using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnController : MonoBehaviour
{
    public EnemyController monster;
    private Vector3 randomPoz;
    private bool onGame = false;
    // Start is called before the first frame update
    void Start()
    {
        onGame = true;
        StartCoroutine(Spawning());
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    IEnumerator Spawning()
    {
        while(onGame)
        {
            yield return new WaitForSeconds(Random.Range(1, 4));
            randomPoz = new Vector3(Random.Range(-5, 5), Random.Range(0.5f, 3), 23);
            Instantiate(monster, randomPoz, Quaternion.Euler(0, 180, 0), transform);
        }
        StopCoroutine(Spawning());
    }
}
