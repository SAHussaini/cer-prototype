# Fork Update

This repository was originally implemented [here](https://github.com/marekzp/islam-debate/) by Marek Zaremba-Pike.

I am extending his work using the [Inspect UK AISI library](https://inspect.aisi.org.uk/) to evaluate the following risks pertaining to LLMs:

- belief bias
- unreasonable religious guidance
- damaging advice (e.g. cultural insensitivity)

This will help prototype the CER Framework I highlighted in [my blog post on NIST AI RMF limitations](https://aamer-ai.blogspot.com/2026/04/nist-framework-thoughts.html).

This is a WIP for my BlueDot TAIS Project; my additions can be found under the 'inspect' folder.

## Implementation Details
CER consists of:
- CATCH near-misses or hits for the risk
- EVALUATE the severity and probability of the risk
- RESPOND with a finetuning patch and reassing risk priorities

In this prototype, we simulate conversations around the three aforementioned risks using Inspect and [HF Transformers API](https://huggingface.co/docs/transformers/index).

## Data
We generate data programmatically with hand-written components. This approach was used instead of deriving synthetic data from LLMs to counter the introduction of erroneous datasets and to also allow for more controllability in tailoring these datasets to target specific areas of concern.

Please refer to /inspect/data to view data generation implementation

## Model
The models used in this study is TBC, but they will be open-source to allow for a finetuning patch as part of the RESPOND phase. I will use HuggingFace Transformers API for finetuning, as it is a simple yet powerful API.

With Inspect, we have made our own multi-dialogue Solver to allow for the conversation to prolong as needed -- this is a more realistic use case. We will also be incorporating a final Scorer as part of EVALUATE, and an intermediate Scorer as part of CATCH. The Scorer models will likely be the same as the user/assistant models.
