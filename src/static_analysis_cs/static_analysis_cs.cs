using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Diagnostics;
using System.Collections.Immutable;
using System;
using System.IO;
using System.Linq;

namespace StaticAnalysis
{
    // 定义一个诊断分析器
    [DiagnosticAnalyzer(LanguageNames.CSharp)]
    public class StaticAnalysisAnalyzer : DiagnosticAnalyzer
    {
        // 定义诊断 ID 和规则
        public const string DiagnosticId = "StaticAnalysisAnalyzer";
        private static readonly DiagnosticDescriptor Rule = new DiagnosticDescriptor(
            DiagnosticId,
            "Potential unhandled exception",
            "This method may throw an exception that is not handled",
            "Usage",
            DiagnosticSeverity.Warning,
            isEnabledByDefault: true);

        // 返回支持的诊断规则
        public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics => ImmutableArray.Create(Rule);

        // 初始化分析器
        public override void Initialize(AnalysisContext context)
        {
            // 注册方法声明的分析
            context.RegisterSyntaxNodeAction(AnalyzeNode, SyntaxKind.MethodDeclaration);
        }

        // 分析方法声明
        private void AnalyzeNode(SyntaxNodeAnalysisContext context)
        {
            var methodDeclaration = (MethodDeclarationSyntax)context.Node;

            // 检查方法是否有 catch 子句
            if (!methodDeclaration.DescendantNodes().OfType<CatchClauseSyntax>().Any())
            {
                // 报告诊断
                var diagnostic = Diagnostic.Create(Rule, methodDeclaration.GetLocation());
                context.ReportDiagnostic(diagnostic);
            }
        }

        // 主程序入口
        public static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            if (args.Length == 0)
            {
                Console.WriteLine("Please provide the path to a C# file.");
                return;
            }

            var filePath = args[0];
            var code = File.ReadAllText(filePath);

            // 解析代码为语法树
            var tree = CSharpSyntaxTree.ParseText(code);
            var compilation = CSharpCompilation.Create("Analysis")
                .AddReferences(MetadataReference.CreateFromFile(typeof(object).Assembly.Location))
                .AddSyntaxTrees(tree);

            // 获取诊断信息
            var diagnostics = compilation.GetDiagnostics();

            // 输出诊断信息
            foreach (var diagnostic in diagnostics)
            {
                Console.WriteLine(diagnostic);
            }
        }
    }
}
