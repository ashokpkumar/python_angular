import { HttpRequest } from '@angular/common/http';
// ...
export class AuthService {
cachedRequests: Array<HttpRequest<any>> = [];
public collectFailedRequest(request): void {
    this.cachedRequests.push(request);
  }
public retryFailedRequests(): void {
    // retry the requests. this method can
    // be called after the token is refreshed
  }
}