import sys
import argparse
import yaml
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).parent))

from core import ChaosMusicCore, ChaosMusicConfig
from core import GenerationPipeline
from core import QualityMetrics


def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config/default.yaml")
    parser.add_argument("--output", type=str, default="output/composition.mid")
    parser.add_argument("--length", type=int, default=100)
    parser.add_argument("--chaos", type=str, default="lorenz")
    parser.add_argument("--scale", type=str, default="major")
    parser.add_argument("--generator", type=str, default="chaotic_melody")
    parser.add_argument("--style", type=str, default="balanced")
    parser.add_argument("--tempo", type=float, default=120.0)
    parser.add_argument("--complexity", type=float, default=0.5)
    parser.add_argument("--batch", type=int, default=0)
    parser.add_argument("--output-dir", type=str, default="output")
    parser.add_argument("--format", type=str, default="midi")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--quality-threshold", type=float, default=0.3)

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        config_data = {}
        if args.config and Path(args.config).exists():
            config_data = load_config(args.config)

        core_config = ChaosMusicConfig()
        if config_data.get('system'):
            if 'log_level' in config_data['system']:
                core_config.log_level = getattr(logging, config_data['system']['log_level'])
            if 'cache_enabled' in config_data['system']:
                core_config.cache_enabled = config_data['system']['cache_enabled'] and not args.no_cache

        core = ChaosMusicCore(core_config)
        core.initialize()

        system_info = core.get_system_info()
        logger.info(f"Chaos systems: {system_info['chaos_systems']}")
        logger.info(f"Scales: {system_info['knowledge_base']['scales']}")
        logger.info(f"Chords: {system_info['knowledge_base']['chords']}")

        if args.batch > 0:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            successful = 0
            for i in range(args.batch):
                logger.info(f"Generating composition {i + 1}/{args.batch}")

                pipeline = core.create_pipeline(args.style)
                if args.chaos != "lorenz":
                    pipeline.chaos_system = args.chaos
                if args.scale != "major":
                    pipeline.music_elements[0]["name"] = args.scale
                pipeline.generation_length = args.length
                pipeline.complexity = args.complexity

                result = core.generate_music(pipeline=pipeline)

                if result["quality_score"] < args.quality_threshold:
                    logger.warning(f"Composition {i + 1} quality too low: {result['quality_score']:.3f}")
                    continue

                output_path = output_dir / f"composition_{i + 1:03d}.mid"
                core.export_composition(result["composition"], args.format, str(output_path))

                logger.info(f"Saved: {output_path} (quality: {result['quality_score']:.3f})")
                successful += 1

            logger.info(f"Batch generation complete: {successful}/{args.batch} successful")

        else:
            if args.chaos != "lorenz" or args.scale != "major":
                chaos_params = {}
                if args.chaos == "lorenz":
                    chaos_params = {"sigma": 10.0, "rho": 28.0, "beta": 2.667}
                elif args.chaos == "rossler":
                    chaos_params = {"a": 0.2, "b": 0.2, "c": 5.7}
                elif args.chaos == "logistic":
                    chaos_params = {"r": 3.99}
                elif args.chaos == "henon":
                    chaos_params = {"a": 1.4, "b": 0.3}
                elif args.chaos == "chua":
                    chaos_params = {"alpha": 15.6, "beta": 28, "m0": -8 / 7, "m1": -5 / 7}
                elif args.chaos == "hyper_lorenz":
                    chaos_params = {"a": 10, "b": 28, "c": 8 / 3, "d": -1}
                else:
                    chaos_params = {}

                pipeline = GenerationPipeline(
                    chaos_system=args.chaos,
                    chaos_parameters=chaos_params,
                    music_elements=[{"type": "scale", "name": args.scale, "root": 60}],
                    mapping_strategy="attractor",
                    generation_length=args.length,
                    complexity=args.complexity,
                    style_constraints={"tempo": args.tempo}
                )
                result = core.generate_music(pipeline=pipeline)
            else:
                result = core.generate_music(style=args.style)

            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            export_path = core.export_composition(result["composition"], args.format, str(output_path))
            logger.info(f"Composition saved to: {export_path}")

            metadata = result["metadata"]
            logger.info(f"Chaos system: {metadata['chaos_system']}")
            logger.info(f"Length: {metadata['generation_length']}")
            logger.info(f"Complexity: {metadata['complexity']:.2f}")
            logger.info(f"Quality score: {result['quality_score']:.3f}")

            if args.analyze:
                analysis = core.analyze_composition(result["composition"])

                logger.info("=== Analysis ===")
                logger.info(f"Notes: {analysis['melodic_analysis']['note_count']}")
                logger.info(f"Pitch range: {analysis['melodic_analysis']['range']} semitones")
                logger.info(f"Melodic contour: {analysis['melodic_analysis']['contour']}")
                logger.info(f"Form type: {analysis['structural_analysis']['form_type']}")
                logger.info(f"Complexity level: {analysis['complexity_level']}")

                quality_metrics = QualityMetrics(
                    melodic_coherence=analysis.get('melodic_coherence', 0.5),
                    harmonic_consonance=analysis.get('harmonic_consonance', 0.5),
                    rhythmic_regularity=analysis.get('rhythmic_regularity', 0.5),
                    formal_structure=analysis.get('formal_structure', 0.5),
                    novelty_score=analysis.get('novelty_score', 0.5),
                    complexity_score=analysis.get('complexity_score', 0.5),
                    musicality_score=result['quality_score']
                )

                logger.info("=== Quality Metrics ===")
                logger.info(f"Melodic coherence: {quality_metrics.melodic_coherence:.3f}")
                logger.info(f"Harmonic consonance: {quality_metrics.harmonic_consonance:.3f}")
                logger.info(f"Rhythmic regularity: {quality_metrics.rhythmic_regularity:.3f}")
                logger.info(f"Formal structure: {quality_metrics.formal_structure:.3f}")
                logger.info(f"Novelty: {quality_metrics.novelty_score:.3f}")
                logger.info(f"Complexity: {quality_metrics.complexity_score:.3f}")
                logger.info(f"Overall musicality: {quality_metrics.musicality_score:.3f}")

        logger.info("Generation complete")

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
