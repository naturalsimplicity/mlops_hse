{{- define "diabetes-ml-chart.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "diabetes-ml-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "diabetes-ml-chart.labels" -}}
app.kubernetes.io/name: {{ include "diabetes-ml-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "diabetes-ml-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "diabetes-ml-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
