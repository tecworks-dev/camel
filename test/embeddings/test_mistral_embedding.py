# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
import os
from unittest.mock import MagicMock, patch

from camel.embeddings import MistralEmbedding


@patch.dict(os.environ, {"MISTRAL_API_KEY": "fake_api_key"})
@patch('mistralai.client.MistralClient', autospec=True)
def test_embed_list(mock_mistral_client):
    # Set up the mock client and its return values
    mock_client_instance = mock_mistral_client.return_value
    mock_client_instance.embeddings.return_value.data = [
        MagicMock(embedding=[0.1, 0.2, 0.3]),
        MagicMock(embedding=[0.4, 0.5, 0.6]),
    ]

    # Instantiate the MistralEmbedding and call embed_list
    embedding = MistralEmbedding()
    result = embedding.embed_list(["text1", "text2"])

    # Validate that embeddings method was called with correct parameters
    mock_client_instance.embeddings.assert_called_once_with(
        input=["text1", "text2"], model="mistral-embed"
    )

    # Validate the result against the mocked data
    assert result == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]


@patch('mistralai.client.MistralClient', autospec=True)
def test_get_output_dim(mock_mistral_client):
    # Instantiate the MistralEmbedding with specified dimensions
    embedding = MistralEmbedding(dimensions=256)

    # Validate that get_output_dim returns the correct value
    assert embedding.get_output_dim() == 256