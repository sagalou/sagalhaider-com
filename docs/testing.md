# Testing

Restituo is tested at three levels: automated tests (pytest-django), continuous integration (GitHub Actions), and manual tests on the deployed site.

## How to run the tests

```bash
source venv/bin/activate
REDIS_DISABLED=1 pytest -v
```

`REDIS_DISABLED=1` replaces Redis with a local in-memory cache, so the tests run without a Redis server.

## Automated tests

**Result: 40 tests, 40 passed** (Python 3.12.3, Django 5.2.17, pytest 9.1.1).

| App | Tests | What is tested |
|---|---|---|
| accounts | 7 | Login page renders; valid password and 2FA code redirect; missing code, wrong code and invalid credentials return 401; non-staff users are rejected; login is rate limited |
| servicerequests | 14 | Valid request returns 201; missing fields return 400; honeypot rejects bots; form is rate limited; dashboard and API require authentication and reject a password-only session (no 2FA); unknown id returns 404; completing a step updates progress; bad payload is rejected; progress calculation; reminders are sent only for requests older than 7 days |
| chatbot | 10 | Empty or malformed message returns 400; FAQ rules are matched before the LLM; graceful fallback without API key; endpoint is rate limited; case-insensitive matching; model tier selection (low, high, unknown falls back to low) |
| core | 6 | Every public page renders: home, sites, cities, contact, about, privacy |
| realisations | 3 | Empty list; created realisations are listed; only GET is allowed |

<details>
<summary>Full pytest output</summary>

```
collected 40 items

accounts/tests.py::TestLogin::test_get_renders_login_page PASSED
accounts/tests.py::TestLogin::test_valid_credentials_and_code_redirect PASSED
accounts/tests.py::TestLogin::test_missing_code_returns_401 PASSED
accounts/tests.py::TestLogin::test_wrong_code_returns_401 PASSED
accounts/tests.py::TestLogin::test_invalid_credentials_return_401 PASSED
accounts/tests.py::TestLogin::test_non_staff_user_rejected PASSED
accounts/tests.py::TestLogin::test_rate_limited_after_threshold PASSED
chatbot/tests.py::TestChatbotEndpoint::test_empty_message_returns_400 PASSED
chatbot/tests.py::TestChatbotEndpoint::test_malformed_json_returns_400 PASSED
chatbot/tests.py::TestChatbotEndpoint::test_faq_rule_matched_before_llm PASSED
chatbot/tests.py::TestChatbotEndpoint::test_no_matching_rule_and_no_api_key_falls_back_gracefully PASSED
chatbot/tests.py::TestChatbotEndpoint::test_rate_limited_after_threshold PASSED
chatbot/tests.py::TestChatbotRuleModel::test_match_is_case_insensitive PASSED
chatbot/tests.py::TestChatbotRuleModel::test_no_match_returns_none PASSED
core/tests.py::TestPublicPages::test_page_renders[home] PASSED
core/tests.py::TestPublicPages::test_page_renders[sites] PASSED
core/tests.py::TestPublicPages::test_page_renders[cities] PASSED
core/tests.py::TestPublicPages::test_page_renders[contact] PASSED
core/tests.py::TestPublicPages::test_page_renders[about] PASSED
core/tests.py::TestPublicPages::test_page_renders[privacy] PASSED
realisations/tests.py::TestRealisationEndpoint::test_empty_list PASSED
realisations/tests.py::TestRealisationEndpoint::test_lists_created_realisations PASSED
realisations/tests.py::TestRealisationEndpoint::test_only_get_allowed PASSED
servicerequests/tests.py::TestCreateRequest::test_valid_submission_returns_201 PASSED
servicerequests/tests.py::TestCreateRequest::test_missing_fields_returns_400 PASSED
servicerequests/tests.py::TestCreateRequest::test_honeypot_rejects_bots PASSED
servicerequests/tests.py::TestCreateRequest::test_rate_limited_after_threshold PASSED
servicerequests/tests.py::TestAdminEndpoints::test_list_requires_auth PASSED
servicerequests/tests.py::TestAdminEndpoints::test_list_rejects_password_only_session PASSED
servicerequests/tests.py::TestAdminEndpoints::test_dashboard_page_requires_2fa PASSED
servicerequests/tests.py::TestAdminEndpoints::test_list_returns_data_when_authenticated PASSED
servicerequests/tests.py::TestAdminEndpoints::test_detail_404_for_unknown_id PASSED
servicerequests/tests.py::TestAdminEndpoints::test_complete_step_updates_progress PASSED
servicerequests/tests.py::TestAdminEndpoints::test_complete_step_rejects_bad_payload PASSED
servicerequests/tests.py::TestServiceRequestModel::test_progress_with_no_steps_is_zero PASSED
servicerequests/tests.py::TestServiceRequestModel::test_progress_counts_completed_steps PASSED
servicerequests/tests.py::test_send_reminders_only_for_overdue_requests PASSED
chatbot/tests.py::TestChatbotModelTierSelection::test_low_tier_selects_haiku PASSED
chatbot/tests.py::TestChatbotModelTierSelection::test_high_tier_selects_sonnet PASSED
chatbot/tests.py::TestChatbotModelTierSelection::test_unknown_tier_falls_back_to_low PASSED

40 passed in 27.24s
```

</details>

## Continuous integration

GitHub Actions runs on every push: first the linters (pycodestyle, pydocstyle), then the full test suite. A failing lint or test blocks the pipeline. See the [Actions tab](https://github.com/sagalou/sagalhaider-com/actions).

## Manual tests (production)

| Test | Input | Expected result | Result |
|---|---|---|---|
| Valid request | POST with name, email, description | 201, request saved, email sent | Pass |
| Missing fields | POST without email | 400, nothing saved | Pass |
| Honeypot | Hidden field filled by a bot | Request rejected | Pass |
| Rate limiting | 6 submissions from the same IP within 1 hour | 429 on the 6th | Pass |
| Access without 2FA | Session with password only | 401 on the request list | Pass |
| Progress | Check 1 step out of 2 | Progress at 50% | Pass |
| 7-day reminder | Two requests, one older than 7 days | Only one reminder sent | Pass |

## Integration checks

- The public form sends JSON to the API and shows the confirmation or the error returned by the server.
- The dashboard loads requests from the API, filters them by status and checks steps without reloading the page; a 401 response redirects to `/login`.
- The chatbot widget sends messages to the API and displays FAQ or LLM answers in FR, EN and SW.
- Checked in the browser DevTools (Network tab): status codes, JSON payloads, CSRF header on admin actions.

## Bugs found and fixed

All bugs are tracked in [GitHub Issues](https://github.com/sagalou/sagalhaider-com/issues?q=is%3Aissue+label%3Abug), each closed with the commit that fixed it.
