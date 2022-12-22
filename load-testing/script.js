import http from 'k6/http';

export default function () {
    // const url = 'https://notes.jesseinit.dev/v1/user/auth/login';
    const url = 'https://notes.jesseinit.dev/v1/user/me';
    // const url = 'http://localhost:8023/v1/user/me';
    // const url = 'http://notes-api:8022/v1/user/me';
    // const url = 'http://notes-api:8022/v1/user/auth/login';
    // const url = 'http://notes-api:8022/v1/note';
    const payload = JSON.stringify({
        username: "bingoman",
        password: "bigmanthing"
    });
    // const payload = JSON.stringify({
    //     "title": "Most of them just Envy",
    // "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mauris cursus mattis molestie a iaculis at erat pellentesque adipiscing"
    //     });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJ1c2VybmFtZSI6ImJpbmdvbWFuIiwiZXhwIjoxNjcxNjQwNTczfQ.CgJtJESaTvvPZoUX7isG9yj9Uq_2e4wIDogEUSsX__0",
    //   "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImU5MzE3MjFlLTZjOGEtNDYxYS05OWVkLWVmYzQ1MTdiYWJjNyIsInVzZXJuYW1lIjoiYmluZ29tYW4iLCJleHAiOjE2NzE1NzUzMjV9.6Dg38sBzgwLUoMsbkgMEHEAuOvSS63bwsLkAtWa14Sg",
    },
  };
  
  http.get(url, params);
  // http.post(url, payload, params);
}
