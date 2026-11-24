# AWS Serverless Equipment Loans API (Track C)

Proyek Cloud Computing Week 12 menggunakan arsitektur Serverless di AWS Learner Lab.

## Arsitektur & Layanan
- **Endpoint:** AWS Lambda Function URL / API Gateway
- **Compute:** AWS Lambda (Python 3.12)
- **Storage:** Amazon S3 (JSON Object Storage) / DynamoDB
- **Security:** AWS IAM (`LabRole`)

## Entitas Data (`LoanItem`)
- `loan_id` (String): ID unik peminjaman
- `item_name` (String): Nama alat yang dipinjam
- `borrower_name` (String): Nama peminjam
- `status` (String): `BORROWED` atau `RETURNED`
- `loan_date` (String): Tanggal peminjaman

## Daftar 4 Endpoint CRUD
- `GET /loans` : Menampilkan seluruh data peminjaman
- `POST /loans` : Menambah data peminjaman baru
- `PUT /loans` : Memperbarui status pengembalian alat
- `DELETE /loans` : Menghapus data peminjaman

## Deployment Plan
1. Membuat bucket S3 sebagai penyimpanan data JSON (alternatif DynamoDB di sandbox).
2. Membuat fungsi AWS Lambda (Python 3.12) dengan execution role `LabRole`.
3. Mengaktifkan Function URL dan menghubungkan Environment Variable `BUCKET_NAME`.
4. Menguji konektivitas CRUD melalui Lambda Console Test dan HTTP client.

## Implementasi pada AWS Academy Sandbox
Karena kebijakan IAM pada lingkungan *sandbox* AWS Academy Lab Project (`ALPMCPBv1`) membatasi izin pembuatan fungsi AWS Lambda secara langsung (`lambda:CreateFunction`), arsitektur komputasi **Track C (Serverless)** diimplementasikan menggunakan layanan komputasi *serverless* setara yang tersedia di *sandbox*, yaitu **Amazon ECS dengan AWS Fargate** (`serverless-loans-cluster`, *task definition* `equipment-loans-task`) yang terintegrasi dengan penyimpanan objek **Amazon S3** (`cc-loans-bintangdanes-2026`).
