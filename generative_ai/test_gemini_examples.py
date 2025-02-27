# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest
import vertexai

import gemini_all_modalities
import gemini_audio
import gemini_chat_example
import gemini_count_token_example
import gemini_grounding_example
import gemini_guide_example
import gemini_multi_image_example
import gemini_pdf_example
import gemini_pro_basic_example
import gemini_pro_config_example
import gemini_safety_config_example
import gemini_single_turn_video_example
import gemini_system_instruction
import gemini_text_input_example
import gemini_video_audio


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)


def test_gemini_guide_example() -> None:
    text = gemini_guide_example.generate_text()
    text = text.lower()
    assert len(text) > 0


def test_gemini_text_input_example() -> None:
    text = gemini_text_input_example.generate_from_text_input()
    assert len(text) > 0


def test_gemini_pro_basic_example() -> None:
    text = gemini_pro_basic_example.generate_text()
    assert len(text) > 0


def test_gemini_pro_config_example() -> None:
    import urllib.request

    #  download the image
    fname = "scones.jpg"
    url = "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg"
    urllib.request.urlretrieve(url, fname)

    if os.path.isfile(fname):
        text = gemini_pro_config_example.generate_text()
        text = text.lower()
        assert len(text) > 0

        # clean-up
        os.remove(fname)
    else:
        raise Exception("File(scones.jpg) not found!")


def test_gemini_multi_image_example() -> None:
    text = gemini_multi_image_example.generate_text_multimodal()
    text = text.lower()
    assert len(text) > 0
    assert "city" in text
    assert "landmark" in text


def test_gemini_count_token_example() -> None:
    response = gemini_count_token_example.count_tokens()
    assert response
    assert response.usage_metadata

    response = gemini_count_token_example.count_tokens_multimodal()
    assert response
    assert response.usage_metadata


def test_gemini_safety_config_example() -> None:
    text = gemini_safety_config_example.generate_text()
    assert len(text) > 0


def test_gemini_single_turn_video_example() -> None:
    text = gemini_single_turn_video_example.generate_text()
    text = text.lower()
    assert len(text) > 0
    assert any(
        [_ in text for _ in ("zoo", "tiger", "leaf", "water", "animals", "photos")]
    )


@pytest.mark.skip(
    "TODO: Exception Logs indicate safety filters are likely blocking model output b/339985493"
)
def test_gemini_pdf_example() -> None:
    text = gemini_pdf_example.analyze_pdf()
    assert len(text) > 0


def test_gemini_chat_example() -> None:
    text = gemini_chat_example.chat_text_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])

    text = gemini_chat_example.chat_stream_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])


# TODO: Delete this file after approval /grounding/web_example.py
@pytest.mark.skip(
    "Unable to test Google Search grounding due to allowlist restrictions."
)
def test_gemini_grounding_web_example() -> None:
    response = gemini_grounding_example.generate_text_with_grounding_web()
    assert response


# TODO: Delete this file after approval /grounding/vais_example.py
def test_gemini_grounding_vais_example() -> None:
    response = gemini_grounding_example.generate_text_with_grounding_vertex_ai_search(
        "grounding-test-datastore"
    )
    assert response


# Delete this test after approval /understand_audio/understand_audio_test.py
def test_summarize_audio() -> None:
    text = gemini_audio.summarize_audio()
    assert len(text) > 0


# Delete this test after approval /understand_audio/understand_audio_test.py
def test_transcript_audio() -> None:
    text = gemini_audio.transcript_audio()
    assert len(text) > 0


def test_analyze_video_with_audio() -> None:
    text = gemini_video_audio.analyze_video_with_audio()
    assert len(text) > 0


def test_analyze_all_modalities() -> None:
    text = gemini_all_modalities.analyze_all_modalities()
    assert len(text) > 0


def test_set_system_instruction() -> None:
    text = gemini_system_instruction.set_system_instruction(PROJECT_ID)
    assert len(text) > 0
