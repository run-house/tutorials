import argparse
import runhouse as rh


# ----------------- README ----------------- #
# Here we simply demonstrate how to use Runhouse to run existing code from Github.

if __name__ == "__main__":
    gpu = rh.cluster(name='rh-a10g', instance_type='A10G:1', provider='cheapest')
    train_gpu = rh.send(fn='https://github.com/huggingface/accelerate/blob/main/examples/nlp_example.py:training_function',
                        hardware=gpu,
                        reqs=['pip:./accelerate', 'evaluate', 'scipy', 'scikit-learn', 'transformers',
                              'torch --upgrade --extra-index-url https://download.pytorch.org/whl/cu116'],
                        name='train_bert_glue')

    train_args = argparse.Namespace(cpu=False, mixed_precision='bf16')
    hps = {"lr": 2e-5, "num_epochs": 3, "seed": 42, "batch_size": 16}
    train_gpu(hps, train_args)

    # Alternatively, we can just run as instructed in the README (but then we leave Python):
    # gpu.run(['python ./nlp_example.py --fp16'])
