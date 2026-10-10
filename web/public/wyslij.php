<?php
// Formularz kontaktowy: wysyła wiadomość na adres lekarza.
$to = 'drmartakryczka@gmail.com';
$isEn = (($_POST['lang'] ?? '') === 'en');
$back = $isEn ? '/en/contact/' : '/kontakt/';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: ' . $back); exit; }

function clean($v, $max) {
    $v = trim((string)$v);
    $v = str_replace(["\r", "\n"], ' ', $v);
    return mb_substr($v, 0, $max);
}
$name = clean($_POST['name'] ?? '', 120);
$email = clean($_POST['email'] ?? '', 160);
$subject = clean($_POST['subject'] ?? '', 160);
$message = trim((string)($_POST['message'] ?? ''));
$message = mb_substr($message, 0, 5000);
$consent = !empty($_POST['consent']);

if (!empty($_POST['website'])) { header('Location: ' . $back . '?status=ok'); exit; }
if ($name === '' || $message === '' || !$consent || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: ' . $back . '?status=blad'); exit;
}

$host = preg_replace('/[^a-z0-9.-]/i', '', $_SERVER['HTTP_HOST'] ?? 'drmartakryczka.pl');
$mailSubject = '=?UTF-8?B?' . base64_encode('Formularz strony: ' . ($subject !== '' ? $subject : ($isEn ? 'message (EN)' : 'wiadomość'))) . '?=';
$body = "Imię i nazwisko: $name\nE-mail: $email\n\n$message\n";
$headers = [
    'From: Strona drmartakryczka.pl <formularz@' . $host . '>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
];
$ok = mail($to, $mailSubject, $body, implode("\r\n", $headers));
header('Location: ' . $back . ($ok ? '?status=ok' : '?status=blad'));
