# 🚀 [내 손 안의 전시회 관람 가이드 앱, Musai]
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/1aed974a-80d1-4c3f-bc97-8a821e9163b2" />

## 📌 개요 (Overview)

> - MUSAI는 AI 기반 작품 인식 기술을 활용해 사용자가 촬영한 작품을 분석하고 자동으로 해설을 제공하는 서비스입니다.
> - 사용자의 관심사(화풍·작가·시대 등)를 기반으로 개인 맞춤형 작품 정보를 추천합니다.
> - AR 기능을 통해 작품의 주요 포인트와 해설 내용을 시각적으로 시각화하여 감상 경험을 확장합니다.
> - 백엔드 서버는 이미지 분석 요청 처리, 작품 정보 제공, 사용자 맞춤 추천 로직 등을 담당해 전체 서비스 흐름을 안정적으로 지원합니다.

---

## 🛠️ 기술 스택 및 개발 환경 (Tech Stack & Environment)

우리 프로젝트를 구축하는 데 사용된 주요 기술과 도구는 다음과 같습니다.

### 💻 클라이언트 및 프론트엔드 (Client & Frontend)

| 분류 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **모바일 앱** | **Flutter** | 크로스 플랫폼 모바일 애플리케이션 개발에 사용 |
| **게임/3D 엔진** | **Unity** | 3D 콘텐츠 및 특수 인터랙션 로직 구현에 사용 |
| **증강 현실 (AR)** | **Vuforia Engine** | 증강 현실 기능 구현 및 트래킹 기술 적용 |

### ⚙️ 백엔드 및 서버 (Backend & Server)

| 분류 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **메인 백엔드** | **Spring Boot** | 주 서비스 로직 및 RESTful API 구축 |
| **AI/ML 서버** | **FastAPI** | 인공지능 모델 호스팅 및 고속 추론 API 제공 |
| **외부 연동** | **외부 AI API** | 특정 고도화된 AI 기능 구현을 위해 외부 서비스 연동 |
| **인증/보안** | **OAuth 2.0 + JWT** | 소셜 로그인 연동 및 토큰 기반 사용자 권한 관리 적용 |
| **메인 데이터베이스** | **AWS RDS MySQL** | 영속적인 데이터 저장 및 관리 (관계형 데이터베이스) |
| **메시징/알림** | **Firebase (FCM)** | 모바일 푸시 알림 서비스 구축 및 관리에 활용 |

### 🌐 배포 및 인프라 (Deployment & Infrastructure)

| 분류 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **클라우드** | **AWS (Amazon Web Services)** | 서버 호스팅 및 인프라 구축 |
| **컨테이너** | **Docker** | 애플리케이션 환경 격리 및 개발/배포 환경 통일 |
| **CI/CD** | **Github Actions** | 자동화된 테스트, 빌드 및 배포 파이프라인 구축 |

### 🤝 협업 및 관리 (Collaboration & Management Tools)

| 분류 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **버전 관리** | **Github** | 소스 코드 관리 및 공유 |
| **이슈 관리** | **Github Issues, Jira** | 버그 추적, 기능 요청, 개발 스프린트 관리 |
| **문서화** | **Notion** | 프로젝트 기획, 회의록, 기술 문서 정리 |
| **커뮤니케이션** | **Discord** | 실시간 팀 커뮤니케이션 및 알림 |
| **디자인** | **Figma** | UI/UX 디자인 및 프로토타이핑 |

---

## 💡 기술 채택 배경 및 개발 철학 (Technology Decisions & Philosophy)

프로젝트에 필요한 핵심 기술을 채택하고 개발을 진행한 배경과 이유는 다음과 같습니다.

### ☕️ Spring Boot (메인 백엔드)

| 결정 이유 | 상세 내용 |
| :--- | :--- |
| **현업 요구사항 및 경험** | Spring Boot는 **현업에서 가장 광범위하게 사용**되는 백엔드 프레임워크 중 하나이며, 팀 내 **Spring 개발 경험**이 있어 안정성과 생산성을 확보했습니다. |
| **강력한 구조** | 대규모 프로젝트를 위한 인증/보안(OAuth 2.0 + JWT), 트랜잭션 관리 등 필요한 기능들을 쉽게 통합하고 확장할 수 있는 **견고한 구조**를 제공합니다. |

### ⚡️ FastAPI (AI 서버)

| 결정 이유 | 상세 내용 |
| :--- | :--- |
| **고성능 및 속도** | FastAPI는 Python 기반 프레임워크 중 **비동기 처리(Async/Await)**를 기본으로 지원하여 **매우 빠른 처리 속도와 높은 동시성**을 제공합니다. 이는 AI 모델 추론처럼 응답 시간이 중요한 서버에 적합합니다. |
| **외부 API 연동 용이성** | FastAPI는 **RESTful API 구축이 간결**하며, **외부 API와 데이터 연동 및 처리가 직관적**입니다. Type Hint 기반으로 자동 생성되는 **Swagger/OpenAPI 문서** 덕분에 연동(외부 AI API 포함)이 용이했습니다. |

### 🐘 AWS RDS MySQL (관계형 데이터베이스)

| 결정 이유 | 상세 내용 |
| :--- | :--- |
| **데이터 정형성** | 프로젝트 데이터가 **명확한 관계를 갖는 정형 데이터** 형태였기 때문에 RDBMS(관계형 데이터베이스)가 적합하다고 판단했습니다. |
| **배포 환경 적합성** | 배포 환경으로 **AWS**를 사용하고 있었으므로, **안정적인 관리형 서비스**인 **AWS RDS**를 통해 **MySQL**을 선택하여 데이터베이스 운영 효율성을 높였습니다. |

### 🛠️ Gradle (빌드 도구)

| 결정 이유 | 상세 내용 |
| :--- | :--- |
| **유연한 의존성 관리** | Flutter, Unity, 외부 AI API 등 **다양한 외부 연동 및 기술 스택**을 사용하는 프로젝트 특성상, **Gradle의 유연하고 빠른 의존성 관리** 시스템이 Maven보다 유리하다고 판단했습니다. |
| **최신 트렌드 반영** | 최신 Spring Boot 프로젝트 및 실무에서도 Maven에서 Gradle로 전환하는 추세가 강해, **개발 생산성 및 미래 유지보수 측면**을 고려했습니다. |

---

## 🌳 브랜치 전략 (Branch Strategy)

프로젝트의 안정적인 개발 및 배포 관리를 위해 **Git-flow 전략을 기반**으로 단순화된 브랜치 운영 방식을 채택했습니다.

### 📝 브랜치 명명 컨벤션

`[타입]/작업내용#이슈번호` 형식으로 브랜치를 생성하여 작업 목적과 연관된 이슈를 명확하게 추적했습니다.

| 타입 (Type) | 목적 | 예시 |
| :--- | :--- | :--- |
| **`feat`** | 새로운 기능(Feature) 개발 | `feat/user-login#15` |
| **`fix`** | 버그 수정 (Bug Fix) | `fix/ar-crash-bug#22` |
| **`refactor`** | 코드 리팩토링 (기능 변경 없이 내부 구조 개선) | `refactor/api-response` |
| **`chore`** | 빌드 시스템, 라이브러리 업데이트 등 자잘한 변경 | `chore/update-gradle` |
| **`test`** | 테스트 코드 추가/수정 | `test/auth-service` |
| **`docs`** | 문서(README, Wiki 등) 관련 변경 | `docs/update-readme` |

### 📌 브랜치 운영 방식

* **`main` 브랜치:**
    * **배포용 브랜치**이며, 서비스에 실제 배포되는 안정적인 코드만을 포함합니다.
* **`develop` 브랜치:**
    * **통합 개발 브랜치**이며, 모든 기능 개발이 완료된 후 `feature` 브랜치에서 Merge 되어 통합 테스트를 진행하는 기준 브랜치입니다.
* **`feature/[기능명]#[이슈번호]` 브랜치 (보조 브랜치):**
    * 기능 단위로 분리된 개발을 진행하며, 개발 완료 후 `develop` 브랜치로 **Pull Request(PR)**를 통해 Merge 요청을 합니다.
 
---

## 📁 디렉토리 구조 (Directory Structure)

본 프로젝트는 Spring Boot의 표준 구조를 따르며, 주요 기능별로 패키지를 분리하여 **SRP(단일 책임 원칙)**를 준수하고 있습니다.

<details>
<summary>🗂️ 프로젝트 파일 구조 보러가기</summary>

```text
├── src
│    ├── main
│    │    ├── java
│    │    │    └── com
│    │    │         └── musai
│    │    │              ├── MusaiApplication.java
│    │    │              ├── config
│    │    │              │    ├── AppConfig.java
│    │    │              │    ├── FirebaseConfig.java
│    │    │              │    ├── S3Config.java
│    │    │              │    ├── SecurityConfig.java
│    │    │              │    ├── SwaggerConfig.java
│    │    │              │    └── WebConfig.java
│    │    │              ├── controller
│    │    │              │    ├── alarm
│    │    │              │    │    └── AlarmController.java
│    │    │              │    ├── ar
│    │    │              │    │    └── ARController.java
│    │    │              │    ├── arts
│    │    │              │    │    ├── ArtController.java
│    │    │              │    │    └── MetController.java
│    │    │              │    ├── auth
│    │    │              │    │    └── AuthController.java
│    │    │              │    ├── bookmark
│    │    │              │    │    └── BookmarkController.java
│    │    │              │    ├── community
│    │    │              │    │    ├── CommentController.java
│    │    │              │    │    ├── LikeController.java
│    │    │              │    │    ├── PostController.java
│    │    │              │    │    ├── PostReportController.java
│    │    │              │    │    ├── UserBlockController.java
│    │    │              │    │    └── UserReportController.java
│    │    │              │    ├── difficulty
│    │    │              │    │    └── DifficultyController.java
│    │    │              │    ├── exhibition
│    │    │              │    │    └── ExhibitionController.java
│    │    │              │    ├── preference
│    │    │              │    │    ├── PreferenceController.java
│    │    │              │    │    └── RecommendController.java
│    │    │              │    ├── recog
│    │    │              │    │    └── RecogController.java
│    │    │              │    ├── swagger
│    │    │              │    │    └── SwaggerRedirectController.java
│    │    │              │    ├── ticket
│    │    │              │    │    └── TicketController.java
│    │    │              │    ├── tts
│    │    │              │    │    └── TtsController.java
│    │    │              │    └── user
│    │    │              │         └── UserController.java
│    │    │              ├── dto
│    │    │              │    ├── alarm
│    │    │              │    │    └── AlarmDTO.java
│    │    │              │    ├── ar
│    │    │              │    │    ├── ARRequestDTO.java
│    │    │              │    │    ├── ARResponseDTO.java
│    │    │              │    │    ├── ArtworkUpdateDTO.java
│    │    │              │    │    └── VuforiaRegisterResponseDTO.java
│    │    │              │    ├── arts
│    │    │              │    │    ├── ArtDto.java
│    │    │              │    │    ├── ImageDto.java
│    │    │              │    │    └── MetDto.java
│    │    │              │    ├── bookmark
│    │    │              │    │    └── BookmarkDTO.java
│    │    │              │    ├── community
│    │    │              │    │    ├── CommentDTO.java
│    │    │              │    │    ├── CommentRequestDTO.java
│    │    │              │    │    ├── CommentUpdateDTO.java
│    │    │              │    │    ├── ImageUploadResponseDTO.java
│    │    │              │    │    ├── LikeDTO.java
│    │    │              │    │    ├── PostDTO.java
│    │    │              │    │    ├── PostReportRequest.java
│    │    │              │    │    ├── PostRequestDTO.java
│    │    │              │    │    ├── PostUpdateDTO.java
│    │    │              │    │    ├── ReportRequest.java
│    │    │              │    │    ├── UserBlockRequest.java
│    │    │              │    │    └── UserBlockResponse.java
│    │    │              │    ├── difficulty
│    │    │              │    │    ├── DifficultyRequestDTO.java
│    │    │              │    │    └── DifficultyResponseDTO.java
│    │    │              │    ├── exhibition
│    │    │              │    │    ├── DetailApiResponse.java
│    │    │              │    │    └── ExhibitionDTO.java
│    │    │              │    ├── preference
│    │    │              │    │    ├── PreferenceDTO.java
│    │    │              │    │    └── RecommendDTO.java
│    │    │              │    ├── recog
│    │    │              │    │    ├── RecogErrorDTO.java
│    │    │              │    │    ├── RecogRequestDTO.java
│    │    │              │    │    ├── RecogResponseDTO.java
│    │    │              │    │    └── VuforiaResponseDTO.java
│    │    │              │    ├── ticket
│    │    │              │    │    ├── ColorDTO.java
│    │    │              │    │    └── TicketDTO.java
│    │    │              │    ├── tts
│    │    │              │    │    ├── TtsRequestDTO.java
│    │    │              │    │    └── TtsResponseDTO.java
│    │    │              │    └── user
│    │    │              │         ├── SettingDTO.java
│    │    │              │         ├── UserDTO.java
│    │    │              │         └── UserErrorDTO.java
│    │    │              ├── entity
│    │    │              │    ├── alarm
│    │    │              │    │    └── Alarm.java
│    │    │              │    ├── ar
│    │    │              │    │    ├── ArArt.java
│    │    │              │    │    └── Point.java
│    │    │              │    ├── arts
│    │    │              │    │    ├── Art.java
│    │    │              │    │    ├── Image.java
│    │    │              │    │    └── Met.java
│    │    │              │    ├── bookmark
│    │    │              │    │    └── Bookmark.java
│    │    │              │    ├── community
│    │    │              │    │    ├── Comment.java
│    │    │              │    │    ├── Like.java
│    │    │              │    │    ├── Post.java
│    │    │              │    │    ├── PostReport.java
│    │    │              │    │    ├── UserBlock.java
│    │    │              │    │    └── UserReport.java
│    │    │              │    ├── exhibition
│    │    │              │    │    ├── ApiFetchStatus.java
│    │    │              │    │    └── Exhibition.java
│    │    │              │    ├── preference
│    │    │              │    │    ├── Preference.java
│    │    │              │    │    └── Recommend.java
│    │    │              │    ├── ticket
│    │    │              │    │    └── Ticket.java
│    │    │              │    └── user
│    │    │              │         ├── DefaultDifficulty.java
│    │    │              │         ├── Setting.java
│    │    │              │         ├── Token.java
│    │    │              │         └── User.java
│    │    │              ├── jwt
│    │    │              │    ├── JwtAuthenticationFilter.java
│    │    │              │    └── JwtTokenProvider.java
│    │    │              ├── repository
│    │    │              │    ├── alarm
│    │    │              │    │    ├── AlarmRepository.java
│    │    │              │    │    └── TokenRepository.java
│    │    │              │    ├── ar
│    │    │              │    │    ├── ArArtRepository.java
│    │    │              │    │    └── PointRepository.java
│    │    │              │    ├── arts
│    │    │              │    │    ├── ArtRepository.java
│    │    │              │    │    ├── ImageRepository.java
│    │    │              │    │    └── MetRepository.java
│    │    │              │    ├── bookmark
│    │    │              │    │    └── BookmarkRepository.java
│    │    │              │    ├── community
│    │    │              │    │    ├── CommentRepository.java
│    │    │              │    │    ├── LikeRepository.java
│    │    │              │    │    ├── PostReportRepository.java
│    │    │              │    │    ├── PostRepository.java
│    │    │              │    │    ├── UserBlockRepository.java
│    │    │              │    │    └── UserReportRepository.java
│    │    │              │    ├── exhibition
│    │    │              │    │    ├── ApiFetchStatusRepository.java
│    │    │              │    │    └── ExhibitionRepository.java
│    │    │              │    ├── preference
│    │    │              │    │    ├── PreferenceRepository.java
│    │    │              │    │    └── RecommendRepository.java
│    │    │              │    ├── ticket
│    │    │              │    │    └── TicketRepository.java
│    │    │              │    └── user
│    │    │              │         ├── SettingRepository.java
│    │    │              │         └── UserRepository.java
│    │    │              ├── scheduler
│    │    │              │    └── ExhibitionScheduler.java
│    │    │              ├── service
│    │    │              │    ├── alarm
│    │    │              │    │    └── AlarmService.java
│    │    │              │    ├── ar
│    │    │              │    │    └── ARService.java
│    │    │              │    ├── arts
│    │    │              │    │    ├── ArtService.java
│    │    │              │    │    └── MetService.java
│    │    │              │    ├── bookmark
│    │    │              │    │    └── BookmarkService.java
│    │    │              │    ├── community
│    │    │              │    │    ├── CommentService.java
│    │    │              │    │    ├── LikeService.java
│    │    │              │    │    ├── PostReportService.java
│    │    │              │    │    ├── PostService.java
│    │    │              │    │    ├── UserBlockService.java
│    │    │              │    │    └── UserReportService.java
│    │    │              │    ├── difficulty
│    │    │              │    │    └── DifficultyService.java
│    │    │              │    ├── exhibition
│    │    │              │    │    └── ExhibitionService.java
│    │    │              │    ├── preference
│    │    │              │    │    ├── PreferenceService.java
│    │    │              │    │    ├── RecommendService.java
│    │    │              │    │    └── RecommendService2.java
│    │    │              │    ├── recog
│    │    │              │    │    ├── RecogService.java
│    │    │              │    │    └── VuforiaService.java
│    │    │              │    ├── ticket
│    │    │              │    │    ├── ColorService.java
│    │    │              │    │    ├── S3Service.java
│    │    │              │    │    └── TicketService.java
│    │    │              │    ├── tts
│    │    │              │    │    └── TtsService.java
│    │    │              │    └── user
│    │    │              │         └── UserService.java
│    │    │              └── util
│    │    │                   ├── AppleClient.java
│    │    │                   ├── AppleJwtUtil.java
│    │    │                   ├── AppleTokenResponse.java
│    │    │                   ├── AppleUserInfo.java
│    │    │                   ├── DetailApiParser.java
│    │    │                   ├── DistanceCalculator.java
│    │    │                   ├── ExhibitionApiParser.java
│    │    │                   ├── ExhibitionApiResponse.java
│    │    │                   └── JwtUtils.java
│    │    └── resources
│    │         ├── firebase
│    │         │    └── firebase-service-account.json
│    │         └── application.properties
└── build.gradle
```
</details>

---

## 🧑‍💻 역할 분담 및 기여 (Roles & Contributions)

본 프로젝트는 효율적인 개발과 책임 분담을 위해 **공통 개발**과 **개별 기여** 영역을 명확히 나누어 진행했습니다.

### 🤝 공통 개발 영역 (Shared Responsibilities)

모든 팀원이 협력하여 아래의 주요 백엔드 기능 개발 및 아키텍처 설계에 참여했습니다.

* **아키텍처 및 설계:** 백엔드 전체 **아키텍처** 및 **ERD 설계** 공동 참여
* **핵심 API 개발 (Spring Boot 기반):**
    * **작품 인식** 및 **AI 해설 생성** 기능
    * **AR 기반 작품 포인트 분석 API**
    * **난이도별 작품 해설** 및 **TTS 변환 API**
    * **전시회 DB 설계** 및 **데이터 수집**
    * **GPS 기반 전시회 추천 API**
    * **사용자 선호도 기반 추천 알고리즘**
    * **티켓 관리** 및 **작품 북마크** 기능
    * **OAuth 기반 회원가입/로그인** 시스템
    * **알림** 및 **푸시 메시지 처리**
    * **커뮤니티 게시글/댓글** API

### 🌟 개별 핵심 기여 (Key Individual Contributions)

| 기여자 | 주요 기여 내용 |
| :--- | :--- |
| **김미현** | * **핵심 기능 제안:** 커뮤니티 기능 제안,  작품 북마크 기능 제안 |
| | * **인프라 구축:** AWS (EC2, RDS, S3) 기반의 안정적인 **3-Tier 아키텍처 인프라** 구축 및 관리 |
| | * **메인 로직 구현:** AR 해설을 위한 **Vuforia Engine Container**와의 연결, **위치 기반 전시회 추천** 알고리즘 개발 |
| | * **인증/보안 로직:** OAuth 2.0 (소셜 로그인) 기반의 JWT 토큰 발급 및 검증 로직을 구현하여 **토큰 기반 인증** 시스템 구축 |
| **류지우** | * **핵심 기능 제안:** AR 기반 작품 해설 기능 아이디어 제안 및 채택, 사용자 맞춤형 작품 추천 기능 제안 및 구현 |
| | * **데이터 구축:** Met API 기반 **28,430개 작품 데이터 수집, 정제 및 테이블 구축** |
| | * **메인 로직 구현:** 작품 인식 및 해설 기능 개발 |
| | * **성능 최적화:** API 응답 속도 **약 40% 최적화**를 통한 사용자 체감 성능 향상 기여 |

---

## 📅 개발 기간 및 작업 관리 (Timeline & Workflow)

### ⏱️ 개발 기간

* **전체 개발 기간:** 2025.04.17 ~ 2025.10.31 (총 **197일**)

### 📈 작업 관리 및 협업 프로세스

* **일정 및 이슈 관리:** **Jira**를 이용하여 **스프린트 및 이슈 관리**를 진행했으며, **Slack**을 통해 실시간 진행 상황 및 알림을 공유했습니다.
* **정기 회의:** **주간 회의**를 정기적으로 진행하며 작업 순서와 우선순위를 조율하고, 각자의 진행 상황과 기술적 이슈를 점검하여 병목 현상을 최소화했습니다.

---

## 🆘 주요 트러블 슈팅 (Major Troubleshooting)

프로젝트 개발 및 배포 과정에서 발생했던 핵심 문제와 이를 해결하며 얻은 교훈은 다음과 같습니다.

### 1️⃣ AWS RDS Private Subnet 배치로 인한 외부 및 EC2 연결 실패

| 구분 | 내용 |
| :--- | :--- |
| **문제 요약** | RDS 인스턴스 생성 후, 로컬 **MySQL Workbench** 접속이 불가능했으며, 배포된 **EC2 서버**에서도 RDS 엔드포인트에 접속할 수 없는 상태가 발생했습니다. |
| **문제 발생 원인** | RDS의 **DB Subnet Group**에 Public/Private 서브넷이 모두 포함되어 있었고, RDS 인스턴스가 **Private Subnet**에 배치되었기 때문입니다. 이로 인해 인터넷 게이트웨이(IGW)를 통한 외부 접속이 불가능해졌습니다. |
| **해결 과정** | 1. **1차 대안 (임시):** 긴급하게 EC2 인스턴스에 SSH 접속 후 CUI 환경에서 RDS에 접속하여 임시 작업 수행. 2. **최종 해결:** **Public Subnet**만 포함하는 새로운 DB Subnet Group을 생성하고, 기존 RDS 인스턴스를 스냅샷 복원 후 **새로운 Public Subnet Group으로 재배치**하여 외부 및 EC2에서의 접속 환경을 확보했습니다. |
| **교훈** | AWS 환경에서 RDS를 외부 또는 Public Subnet의 EC2에서 직접 접근하려면, **Public Subnet만으로 구성된 Subnet Group**을 명시적으로 생성하고 사용해야 합니다. |

### 2️⃣ Google Vision API 호출 최적화를 통한 인식 속도 개선

| 구분 | 내용 |
| :--- | :--- |
| **문제 요약** | 이미지 인식을 위해 Google Cloud Vision API의 `web_detection` 기능을 사용했으나, **Best Guess Label**과 **원본 URL**을 각각 별도 함수로 호출하는 구조 때문에 **응답 지연(평균 3~5초 이상)** 및 **중복 API 호출 비용** 문제가 발생했습니다. |
| **문제 발생 원인** | `web_detection`을 여러 번 호출하여 리소스 낭비가 발생했고, 작품 제목 추출 로직(Best Guess, 웹 엔티티, 페이지 제목)이 여러 함수에 분산되어 있어 라우터에서의 **중복 처리 및 복잡도가 증가**했습니다. |
| **해결 과정** | 1. **호출 단일화:** 한 번의 `client.web_detection(image=image)` 호출로 **원본 이미지 URL, Best Guess Label, title 후보**를 모두 추출하도록 로직을 통합했습니다. 2. **Title 결정 로직 개선:** 웹 엔티티, 페이지 제목, Best Guess Label 순으로 **우선순위 기반 단일 결정 로직**을 적용하여 작품 제목 추출 정확도를 높였습니다. 3. **모듈화:** 모든 처리를 `get_image_analysis(image_data)` 단일 함수로 캡슐화하여 라우터의 재사용성과 유지보수성을 극대화했습니다. |
| **교훈** | 외부 API 사용 시 **최대한 적은 횟수의 호출**로 필요한 모든 데이터를 가져와 **내부에서 처리하는 방식**이 성능과 비용 측면에서 가장 효율적이며, 이를 통해 **응답 속도를 2배 이상 개선**할 수 있었습니다. |

---

## ✨ 주요 기능 및 페이지 (Features by Page)

### 🔑 로그인 및 초기 설정
| 화면 이미지 | 주요 기능 및 설명 |
| :---: | :--- |
| <img src="https://github.com/user-attachments/assets/90d74711-24b8-442f-a5b7-18e4f2f2ec03" width="180"/> | **소셜 로그인 (Login)**<br><br> - **OAuth 2.0 기반 인증**: Google, Apple 등 소셜 계정을 통한 간편한 회원가입 및 로그인 지원<br> - **보안**: JWT(JSON Web Token)를 활용한 안전한 사용자 인증 및 세션 관리 |
| <img src="https://github.com/user-attachments/assets/1f373793-4f7a-4d08-aedc-a06ddb1ad68c" width="180"/> | **취향 테스트 (Preference Test)**<br><br> - **선호도 분석**: 초기 가입 시 작품 선호도 테스트를 통해 사용자의 예술적 취향 파악<br> - **추천 알고리즘**: 테스트 결과를 기반으로 개인화된 초기 작품 및 전시 추천 데이터 생성 |

### 🏠 메인 및 전시 추천
| 화면 이미지 | 주요 기능 및 설명 |
| :---: | :--- |
| <img src="https://github.com/user-attachments/assets/e12939ac-af30-4427-8ab9-6d41fb0f9759" width="180"/> | **메인 홈 (Home)**<br><br> - **GPS 기반 위치 추천**: 사용자의 현재 위치를 기반으로 가장 가까운 전시회 및 미술관 정보 제공<br> - **맞춤형 큐레이션**: 취향 테스트 결과 및 활동 데이터를 분석하여 사용자 맞춤형 작품 리스트 노출 |

### 📸 작품 인식 및 AI 도슨트
| 화면 이미지 | 주요 기능 및 설명 |
| :---: | :--- |
| <img src="https://github.com/user-attachments/assets/5e10d3de-bb1c-445b-98f4-57b15631cf46" width="180"/> <img src="https://github.com/user-attachments/assets/0e7713be-d1e3-40ff-945d-549e87ac8fba" width="180"/> | **카메라 기반 작품 인식 & 해설**<br><br> - **실시간 스캐닝**: 카메라로 작품을 비추면 AI 서버(FastAPI)가 실시간으로 작품 정보 판별<br> - **맞춤형 해설**: 사용자 설정에 따른 **난이도별(어린이/일반/전문가)** 텍스트 해설 제공<br> - **TTS 서비스**: 인식된 해설 내용을 음성으로 변환하여 오디오 가이드 제공<br> - **북마크**: 마음에 드는 작품을 즉시 저장하여 나중에 다시 확인 가능 |

### 🕶️ AR 도슨트 서비스
| 화면 이미지 | 주요 기능 및 설명 |
| :---: | :--- |
| <img src="https://github.com/user-attachments/assets/0641d15e-f4ab-45eb-b89f-9255f46a8e8e" width="180"/> | **AR 작품 도슨트 (AR Docent)**<br><br> - **인터랙티브 포인트**: Vuforia를 통해 작품 내 핵심 감상 포인트를 AR 마커로 시각화<br> - **몰입형 경험**: 실제 작품 위에 오버레이되는 디지털 정보를 통해 깊이 있는 작품 감상 지원 |

### 🎫 마이페이지 및 커뮤니티
| 화면 이미지 | 주요 기능 및 설명 |
| :---: | :--- |
| <img src="https://github.com/user-attachments/assets/be292214-203a-453e-97e4-1598736d4f7e" width="180"/> | **북마크 및 디지털 티켓**<br><br> - **개인 보관함**: 저장한 작품들을 한눈에 모아보고 다시 감상할 수 있는 북마크 기능<br> - **디지털 티켓**: 북마크한 작품이나 관람 전시를 고유한 디자인의 **디지털 티켓**으로 자동 생성 및 소장 |
| <img src="https://github.com/user-attachments/assets/5c9e5e78-6c8a-4860-a8d6-f584d5e865fe" width="180"/> | **커뮤니티 (Community)**<br><br> - **사용자 소통**: 전시 후기 공유, 정보 교환 등 사용자 간 자유로운 커뮤니케이션 공간 제공<br> - **상호작용**: 게시글 작성, 댓글, 좋아요 기능을 통한 예술 커뮤니티 활성화 |

---

## 📈 향후 개선 사항 (Future Improvements)

| 분류 | 내용 |
| :--- | :--- |
| **성능 최적화** | Redis 캐싱 도입을 통한 DB 부하 감소 및 조회 성능 향상 |
| **인프라** | Prometheus & Grafana를 활용한 서버 모니터링 시스템 구축 |
| **AI 고도화** | 사용자 행동 패턴 분석을 통한 딥러닝 기반 맞춤형 추천 엔진 도입 |
| **사용성 개선** | 글로벌 사용자를 위한 다국어 자동 번역 및 로컬라이징 지원 |

---

## 📥 애플리케이션 다운로드

지금 바로 App Store에서 **Musai**를 만나보세요!

<a href="https://apps.apple.com/kr/app/musai/id6753198681?l=en-GB">
  <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" width="160">
</a>
