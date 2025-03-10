from typing import List, Dict, Optional
from pydantic import BaseModel, computed_field, Field


MILLION: int = 1_000_000


class Pricing(BaseModel):
    input_per_1M_tokens: Optional[float] = None
    cached_input_per_1M_tokens: Optional[float] = None
    output_per_1M_tokens: Optional[float] = None
    cost_per_1M_tokens: Optional[float] = None

    @computed_field
    @property
    def input_price(self) -> float:
        return self.input_per_1M_tokens / MILLION

    @computed_field
    @property
    def cached_input_price(self) -> float:
        if not self.cached_input_per_1M_tokens:
            raise ValueError()
        return self.cached_input_per_1M_tokens / MILLION
    
    @computed_field
    @property
    def output_price(self) -> float:
        return self.output_per_1M_tokens / MILLION

    @computed_field
    @property
    def cost(self) -> float:
        if not self.cost_per_1M_tokens:
            raise ValueError()
        return self.cost_per_1M_tokens / MILLION


class GPTModel(BaseModel):
    name: str
    pricing: Pricing

gpt_models: List[GPTModel] = [
    GPTModel(name="gpt-o1", pricing=Pricing(input_per_1M_tokens=15.00, cached_input_per_1M_tokens=7.50, output_per_1M_tokens=60.00)),
    GPTModel(name="gpt-o3-mini", pricing=Pricing(input_per_1M_tokens=1.10, cached_input_per_1M_tokens=0.55, output_per_1M_tokens=4.40)),
    GPTModel(name="gpt-o1-mini", pricing=Pricing(input_per_1M_tokens=1.10, cached_input_per_1M_tokens=0.55, output_per_1M_tokens=4.40)),
    GPTModel(name="gpt-4.5", pricing=Pricing(input_per_1M_tokens=75.00, cached_input_per_1M_tokens=37.50, output_per_1M_tokens=150.00)),
    GPTModel(name="gpt-4o", pricing=Pricing(input_per_1M_tokens=2.50, cached_input_per_1M_tokens=1.25, output_per_1M_tokens=10.00)),
    GPTModel(name="gpt-4o-mini", pricing=Pricing(input_per_1M_tokens=0.150, cached_input_per_1M_tokens=0.075, output_per_1M_tokens=0.600)),
    GPTModel(name="gpt-4-turbo", pricing=Pricing(input_per_1M_tokens=10.00, output_per_1M_tokens=30.00)),
    GPTModel(name="gpt-4", pricing=Pricing(input_per_1M_tokens=30.00, output_per_1M_tokens=60.00)),
    GPTModel(name="gpt-3.5-turbo", pricing=Pricing(input_per_1M_tokens=0.50, output_per_1M_tokens=1.50)),
    GPTModel(name="text-embedding-3-small", pricing=Pricing(cost_per_1M_tokens=0.02)),
    GPTModel(name="text-embedding-3-large", pricing=Pricing(cost_per_1M_tokens=0.13)),
    GPTModel(name="text-embedding-ada-002", pricing=Pricing(cost_per_1M_tokens=0.10))
]

# 이름 기반으로 모델을 찾을 수 있도록 딕셔너리 생성
gpt_model_dict: Dict[str, GPTModel] = {model.name: model for model in gpt_models}



class EncodingModel(BaseModel):
    name: str
    models: List[GPTModel]

# 모델 이름을 `GPTModel` 객체로 변환하는 함수
def get_models_by_names(model_names: List[str]) -> List[GPTModel]:
    return [gpt_model_dict[name] for name in model_names if name in gpt_model_dict]

encodings: List[EncodingModel] = [
    EncodingModel(name="o200k_base", models=get_models_by_names(["gpt-4o", "gpt-4o-mini"])),
    EncodingModel(name="cl100k_base", models=get_models_by_names(["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"])),
    EncodingModel(name="p50k_base", models=get_models_by_names(["text-davinci-002", "text-davinci-003"])),
    EncodingModel(name="r50k_base", models=get_models_by_names(["davinci"])),
    EncodingModel(name="gpt2", models=get_models_by_names(["davinci"]))
]