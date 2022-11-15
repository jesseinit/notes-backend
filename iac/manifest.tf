resource "helm_release" "notes-api-ingress-nginx" {
  name             = "ingress-nginx"
  chart            = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  version          = "4.4.0"
  namespace        = "ingress-nginx"
  create_namespace = true

}

resource "helm_release" "notes-api-cert-manager" {
  name             = "cert-manager"
  chart            = "cert-manager"
  repository       = "https://charts.jetstack.io"
  version          = "1.10.0"
  namespace        = "cert-manager"
  create_namespace = true

  set {
    name  = "installCRDs"
    value = "true"
  }

  set {
    name  = "startupapicheck.timeout"
    value = "5m"
  }

}

data "kubectl_file_documents" "database" {
  content = file("../k8s/remote/database.yml")
}
resource "kubectl_manifest" "database" {
  for_each  = data.kubectl_file_documents.database.manifests
  yaml_body = each.value
}

data "kubectl_file_documents" "remote-notes-api" {
  content = file("../k8s/remote/remote-notes-api.yml")
}
resource "kubectl_manifest" "remote-notes-api" {
  for_each  = data.kubectl_file_documents.remote-notes-api.manifests
  yaml_body = each.value
}

data "kubectl_file_documents" "remote-le-cluster-issuer" {
  content = file("../k8s/remote/remote-le-cluster-issuer.yaml")
}
resource "kubectl_manifest" "remote-le-cluster-issuer" {
  for_each  = data.kubectl_file_documents.remote-le-cluster-issuer.manifests
  yaml_body = each.value
  depends_on = [
    helm_release.notes-api-cert-manager
  ]
}

data "kubectl_file_documents" "remote-ingress" {
  content = file("../k8s/remote/remote-ingress.yml")
}
resource "kubectl_manifest" "remote-ingress" {
  for_each  = data.kubectl_file_documents.remote-ingress.manifests
  yaml_body = each.value
}
